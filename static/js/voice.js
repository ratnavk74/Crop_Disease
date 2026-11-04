/**
 * CropShield AI - Voice Assistant
 * --------------------------------------------------------------------------
 * Farmers can speak in English, Hindi or Kannada. The browser performs
 * speech-to-text (Web Speech API), the recognised sentence is answered by the
 * local Flask /api/assistant endpoint, and the reply is spoken back with the
 * SpeechSynthesis API.
 *
 * Requirements: Chrome or Edge, microphone permission, and localhost/HTTPS.
 */

(function () {
    'use strict';

    const CFG = window.CROPSHIELD || {};
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const TTS = 'speechSynthesis' in window;

    const ui = {
        widget: null,
        panel: null,
        fab: null,
        close: null,
        status: null,
        transcript: null,
        transcriptText: null,
        reply: null,
        replyText: null,
        listenBtn: null,
        listenLabel: null
    };

    let recognition = null;
    let listening = false;
    let busy = false;
    let lastRequestId = 0;
    let recognitionSession = 0;

    function t(key, fallback) {
        const value = CFG.i18n && CFG.i18n[key];
        return value || fallback || '';
    }

    function init() {
        ui.widget = document.getElementById('voiceWidget');
        if (!ui.widget) return;

        ui.panel = document.getElementById('voicePanel');
        ui.fab = document.getElementById('voiceFab');
        ui.close = document.getElementById('voiceClose');
        ui.status = document.getElementById('voiceStatus');
        ui.transcript = document.getElementById('voiceTranscript');
        ui.transcriptText = document.getElementById('voiceTranscriptText');
        ui.reply = document.getElementById('voiceReply');
        ui.replyText = document.getElementById('voiceReplyText');
        ui.listenBtn = document.getElementById('voiceListenBtn');
        ui.listenLabel = ui.listenBtn ? ui.listenBtn.querySelector('.voice-listen-label') : null;

        bindEvents();
        setStatus(t('help', ''));

        if (!SpeechRecognition) {
            showUnsupported();
        }
    }

    function bindEvents() {
        // Open / close button in the navigation or floating action button.
        document.querySelectorAll('[data-voice-toggle]').forEach(function (button) {
            button.addEventListener('click', function () {
                if (isPanelOpen()) {
                    closePanel();
                } else {
                    openPanel();
                }
            });
        });

        if (ui.close) {
            ui.close.addEventListener('click', closePanel);
        }

        // Every "Speak" / "Ask by voice" button opens the panel and starts the mic.
        document.querySelectorAll('[data-voice-start]').forEach(function (button) {
            button.addEventListener('click', function () {
                openPanel();
                if (listening) {
                    stopListening();
                } else {
                    startListening();
                }
            });
        });

        // Example phrases: send them to the assistant without using the mic.
        document.querySelectorAll('[data-voice-example]').forEach(function (chip) {
            chip.addEventListener('click', function () {
                const phrase = chip.getAttribute('data-voice-example') || chip.textContent;
                openPanel();
                askAssistant(phrase.trim());
            });
        });

        // "Listen to steps" button on the diagnosis report.
        document.querySelectorAll('[data-voice-steps]').forEach(function (button) {
            button.addEventListener('click', function () {
                readStepsAloud();
            });
        });

        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' && isPanelOpen()) {
                closePanel();
            }
        });

        // Some browsers expose voices only after the first interaction.
        if (TTS) {
            window.speechSynthesis.getVoices();
        }
    }

    function isPanelOpen() {
        return !!ui.panel && !ui.panel.classList.contains('hidden');
    }

    function openPanel() {
        if (!ui.panel) return;
        ui.panel.classList.remove('hidden');
        if (ui.fab) ui.fab.setAttribute('aria-expanded', 'true');
        ui.panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function closePanel() {
        if (!ui.panel) return;
        ui.panel.classList.add('hidden');
        if (ui.fab) ui.fab.setAttribute('aria-expanded', 'false');
        stopListening();
        if (TTS) window.speechSynthesis.cancel();
    }

    function showUnsupported() {
        setStatus(t('voiceNotSupported', 'Speech recognition needs Chrome or Edge.'), true);
        if (ui.listenBtn) {
            ui.listenBtn.classList.add('is-disabled');
            ui.listenBtn.setAttribute('disabled', 'disabled');
        }
    }

    function setStatus(message, isError) {
        if (!ui.status) return;
        ui.status.textContent = message || '';
        ui.status.classList.toggle('voice-status-error', !!isError);
    }

    function setListeningState(active) {
        listening = active;
        if (ui.listenBtn) {
            ui.listenBtn.classList.toggle('listening', active);
            const icon = ui.listenBtn.querySelector('i');
            if (icon) {
                icon.className = active ? 'fa-solid fa-stop' : 'fa-solid fa-microphone';
            }
        }
        if (ui.listenLabel) {
            ui.listenLabel.textContent = active
                ? t('stop', 'Stop')
                : t('start', 'Speak');
        }
        if (ui.widget) {
            ui.widget.classList.toggle('is-listening', active);
        }
    }

    function showTranscript(text) {
        if (!ui.transcript || !ui.transcriptText) return;
        ui.transcriptText.textContent = text || '';
        ui.transcript.classList.toggle('hidden', !text);
    }

    function showReply(text) {
        if (!ui.reply || !ui.replyText) return;
        ui.replyText.textContent = text || '';
        ui.reply.classList.toggle('hidden', !text);
    }

    function startListening() {
        if (busy) return;

        if (!SpeechRecognition) {
            showUnsupported();
            return;
        }
        if (!window.isSecureContext && window.location.hostname !== 'localhost' &&
            window.location.hostname !== '127.0.0.1') {
            setStatus(t('permissionDenied', 'Microphone access needs HTTPS or localhost.'), true);
            return;
        }

        // Cancel any previous session before starting a fresh one. Creating a
        // new recogniser each time avoids stale language settings in Chrome.
        recognitionSession += 1;
        const sessionId = recognitionSession;
        if (recognition) {
            try { recognition.abort(); } catch (err) { /* ignore */ }
            recognition = null;
        }

        let finalText = '';
        let interimText = '';

        try {
            recognition = new SpeechRecognition();
        } catch (err) {
            setStatus(t('voiceNotSupported', 'Speech recognition is not available.'), true);
            return;
        }

        recognition.lang = CFG.speechLang || 'en-IN';
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.maxAlternatives = 1;

        recognition.onstart = function () {
            if (sessionId !== recognitionSession) return;
            setListeningState(true);
            setStatus(t('listening', 'Listening…'), false);
            showReply('');
        };

        recognition.onresult = function (event) {
            if (sessionId !== recognitionSession) return;
            interimText = '';
            for (let i = event.resultIndex; i < event.results.length; i += 1) {
                const result = event.results[i];
                const transcript = result[0] ? result[0].transcript : '';
                if (result.isFinal) {
                    finalText += transcript;
                } else {
                    interimText += transcript;
                }
            }
            const preview = (finalText + ' ' + interimText).trim();
            if (preview) showTranscript(preview);
        };

        recognition.onerror = function (event) {
            if (sessionId !== recognitionSession) return;
            const code = event.error || '';
            if (code === 'aborted') return;

            const messages = {
                'not-allowed': t('permissionDenied', 'Microphone permission was denied.'),
                'service-not-allowed': t('permissionDenied', 'Microphone permission was denied.'),
                'audio-capture': t('permissionDenied', 'No microphone was found.'),
                'no-speech': t('noSpeech', 'I could not hear anything. Please try again.'),
                'network': t('error', 'Network error. Please try again.'),
                'language-not-supported': t('voiceNotSupported', 'This language is not supported by your browser.')
            };
            setStatus(messages[code] || t('error', 'Something went wrong. Please try again.'), true);
        };

        recognition.onend = function () {
            if (sessionId !== recognitionSession) return;
            setListeningState(false);
            const spoken = (finalText || interimText).trim();
            recognition = null;

            if (!spoken) {
                if (ui.status && !ui.status.classList.contains('voice-status-error')) {
                    setStatus(t('noSpeech', 'I could not hear anything. Please try again.'), true);
                }
                return;
            }

            askAssistant(spoken);
        };

        try {
            showTranscript('');
            setStatus(t('listening', 'Listening…'), false);
            recognition.start();
        } catch (err) {
            setListeningState(false);
            setStatus(t('error', 'Could not start the microphone. Please try again.'), true);
        }
    }

    function stopListening() {
        recognitionSession += 1;
        if (!recognition) {
            setListeningState(false);
            return;
        }
        try {
            recognition.abort();
        } catch (err) {
            /* ignore */
        }
        recognition = null;
        setListeningState(false);
        setStatus(t('help', ''), false);
    }

    function askAssistant(text) {
        if (!text) return;

        const requestId = lastRequestId + 1;
        lastRequestId = requestId;

        busy = true;
        showTranscript(text);
        showReply('');
        setStatus(t('processing', 'Thinking…'), false);
        if (ui.listenBtn) ui.listenBtn.classList.add('is-busy');

        const payload = {
            text: text,
            lang: CFG.lang || 'en',
            page: CFG.page || 'home',
            disease: CFG.diseaseKey || null,
            confidence: CFG.confidence || null
        };

        fetch(CFG.urls && CFG.urls.assistant ? CFG.urls.assistant : '/api/assistant', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
            credentials: 'same-origin'
        })
            .then(function (response) {
                if (!response.ok) throw new Error('Assistant HTTP ' + response.status);
                return response.json();
            })
            .then(function (data) {
                if (requestId !== lastRequestId) return;
                const reply = (data && data.reply) || t('error', 'Something went wrong.');
                showReply(reply);

                if (data && data.speak !== false) {
                    speak(reply);
                }

                if (data && data.action) {
                    handleAction(data.action, data.target);
                }
            })
            .catch(function () {
                if (requestId !== lastRequestId) return;
                const message = t('error', 'Sorry, I could not process that. Please try again.');
                showReply(message);
                setStatus(message, true);
                speak(message);
            })
            .finally(function () {
                if (requestId !== lastRequestId) return;
                busy = false;
                if (ui.listenBtn) ui.listenBtn.classList.remove('is-busy');
                if (ui.status && !ui.status.classList.contains('voice-status-error')) {
                    setStatus(t('help', ''), false);
                }
            });
    }

    function speak(text) {
        if (!text) return;
        if (!TTS) {
            return;
        }
        if (typeof window.speakText === 'function') {
            window.speakText(text, CFG.lang || 'en');
            return;
        }

        // Fallback if main.js failed to load.
        try {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = CFG.speechLang || 'en-IN';
            utterance.rate = 0.92;
            window.speechSynthesis.speak(utterance);
        } catch (err) {
            /* ignore */
        }
    }

    function handleAction(action, target) {
        switch (action) {
            case 'set_language':
                if (target) {
                    const template = (CFG.urls && CFG.urls.setLanguage) || '/set-language/__LANG__';
                    const next = encodeURIComponent(window.location.pathname + window.location.search);
                    window.location.href = template.replace('__LANG__', target) + '?next=' + next;
                }
                break;

            case 'logout':
                if (CFG.urls && CFG.urls.logout) {
                    window.location.href = CFG.urls.logout;
                }
                break;

            case 'navigate':
                if (target === 'login' && CFG.urls && CFG.urls.login) {
                    window.location.href = CFG.urls.login;
                } else if (CFG.urls && CFG.urls.home) {
                    if (window.location.pathname === '/' || window.location.pathname === '') {
                        window.location.hash = '';
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                    } else {
                        window.location.href = CFG.urls.home;
                    }
                }
                break;

            case 'open_upload':
                openUploader();
                break;

            case 'speak_advisory':
                readAdvisoryAloud();
                break;

            case 'read_steps':
                document.querySelectorAll('.prevention-step').forEach(function (step) {
                    step.classList.add('step-highlight');
                });
                readStepsAloud();
                break;

            default:
                break;
        }
    }

    function openUploader() {
        const upload = document.getElementById('upload');
        if (!upload) {
            if (CFG.urls && CFG.urls.home) {
                window.location.href = CFG.urls.home + '#upload';
            }
            return;
        }

        closePanel();
        upload.scrollIntoView({ behavior: 'smooth', block: 'start' });

        const dropZone = document.getElementById('dropZone');
        if (dropZone) {
            dropZone.classList.add('drop-zone-pulse');
            window.setTimeout(function () {
                dropZone.classList.remove('drop-zone-pulse');
            }, 2200);
        }

        const fileInput = document.getElementById('fileInput');
        if (fileInput) {
            window.setTimeout(function () { fileInput.click(); }, 500);
        }
    }

    function readAdvisoryAloud() {
        if (typeof window.playVoice === 'function') {
            window.playVoice(CFG.lang || 'en');
            return;
        }

        const ids = { en: 'voiceScriptEn', hi: 'voiceScriptHi', kn: 'voiceScriptKn' };
        const element = document.getElementById(ids[CFG.lang || 'en']);
        if (element && element.textContent.trim()) {
            speak(element.textContent.trim());
        } else {
            setStatus(t('error', 'No audio advisory is available on this page.'), true);
        }
    }

    function readStepsAloud() {
        const steps = Array.prototype.map.call(
            document.querySelectorAll('.prevention-step .step-text'),
            function (step, index) { return (index + 1) + '. ' + step.textContent.trim(); }
        );
        if (steps.length) {
            speak(steps.join(' '));
        } else {
            setStatus(t('error', 'No prevention steps are available on this page.'), true);
        }
    }

    // The script can be loaded after DOMContentLoaded in some cached pages.
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose a tiny API so buttons rendered later can use the assistant.
    window.CropShieldVoice = {
        open: openPanel,
        close: closePanel,
        listen: startListening,
        stop: stopListening,
        ask: askAssistant
    };
})();
