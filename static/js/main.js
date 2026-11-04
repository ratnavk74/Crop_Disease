/**
 * CropShield AI - Interactive Client Scripts
 * Handles:
 * - Drag & drop file uploads and real-time image preview
 * - Submit state and loading indicator
 * - Language switching (with automatic browser-language detection server-side)
 * - Password visibility, demo-login fill and flash messages
 * - Multi-language speech synthesis audio advisory (EN, HI, KN)
 */

document.addEventListener('DOMContentLoaded', () => {
    initDropZone();
    initFormSubmit();
    initLanguageSwitcher();
    initPasswordToggles();
    initDemoLogin();
    initFlashMessages();
    initRegistrationForm();
});

const CFG = window.CROPSHIELD || {};

// ==========================================================================
// Drag & Drop and Preview Handlers
// ==========================================================================
function initDropZone() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const dropPrompt = document.getElementById('dropZonePrompt');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const previewFilename = document.getElementById('previewFilename');
    const btnRemove = document.getElementById('btnRemovePreview');

    if (!dropZone || !fileInput) return;

    // Drag-over styling
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('dragover');
        });
    });

    // Handle dropped files
    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files && files.length > 0) {
            fileInput.files = files;
            displayPreview(files[0]);
        }
    });

    // Handle standard file selection
    fileInput.addEventListener('change', () => {
        if (fileInput.files && fileInput.files[0]) {
            displayPreview(fileInput.files[0]);
        }
    });

    // Remove preview
    if (btnRemove) {
        btnRemove.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            fileInput.value = '';
            imagePreview.src = '';
            previewContainer.classList.add('hidden');
            dropPrompt.classList.remove('hidden');
        });
    }

    function displayPreview(file) {
        if (!file.type.match('image.*')) {
            alert(CFG.i18n?.invalidImage || 'Please select a valid image file (JPG, PNG, WEBP).');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            previewFilename.textContent = file.name;
            dropPrompt.classList.add('hidden');
            previewContainer.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
}

// ==========================================================================
// Form Submission & Loading Spinner
// ==========================================================================
function initFormSubmit() {
    const form = document.getElementById('uploadForm');
    const btnSubmit = document.getElementById('btnSubmit');
    const btnText = document.querySelector('.btn-text');
    const btnLoader = document.getElementById('btnLoader');

    if (form && btnSubmit) {
        form.addEventListener('submit', () => {
            btnSubmit.disabled = true;
            if (btnText) btnText.classList.add('hidden');
            if (btnLoader) btnLoader.classList.remove('hidden');
        });
    }
}

// ==========================================================================
// Language switcher (auto-detection happens on the server)
// ==========================================================================
function initLanguageSwitcher() {
    const select = document.getElementById('languageSelect');
    if (!select) return;

    select.addEventListener('change', () => {
        const template = CFG.urls?.setLanguage || '/set-language/__LANG__';
        const next = encodeURIComponent(window.location.pathname + window.location.search);
        window.location.href = template.replace('__LANG__', select.value) + '?next=' + next;
    });
}

// ==========================================================================
// Password visibility and demo login helpers
// ==========================================================================
function initPasswordToggles() {
    document.querySelectorAll('[data-password-toggle]').forEach(button => {
        button.addEventListener('click', () => {
            const target = document.querySelector(button.getAttribute('data-password-toggle'));
            if (!target) return;
            const showing = target.type === 'text';
            target.type = showing ? 'password' : 'text';
            const icon = button.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-eye', showing);
                icon.classList.toggle('fa-eye-slash', !showing);
            }
            button.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
        });
    });
}

function initDemoLogin() {
    const button = document.querySelector('[data-demo-identifier]');
    if (!button) return;

    button.addEventListener('click', () => {
        const identifier = document.getElementById('identifier');
        const password = document.getElementById('password');
        if (identifier) {
            identifier.value = button.getAttribute('data-demo-identifier') || '';
            identifier.focus();
        }
        if (password) {
            password.value = button.getAttribute('data-demo-password') || '';
        }
        button.classList.add('demo-filled');
    });
}

function initFlashMessages() {
    document.querySelectorAll('.flash-message').forEach(message => {
        const close = message.querySelector('.flash-close');
        if (close) {
            close.addEventListener('click', () => message.remove());
        }
        window.setTimeout(() => {
            message.classList.add('flash-fade');
            window.setTimeout(() => message.remove(), 400);
        }, 7000);
    });
}

function initRegistrationForm() {
    const form = document.getElementById('registerForm');
    if (!form) return;

    form.addEventListener('submit', (event) => {
        const password = document.getElementById('password');
        const confirm = document.getElementById('confirm_password');
        if (password && confirm && password.value !== confirm.value) {
            event.preventDefault();
            confirm.setCustomValidity('Passwords do not match');
            confirm.reportValidity();
        }
    });

    const confirm = document.getElementById('confirm_password');
    if (confirm) {
        confirm.addEventListener('input', () => confirm.setCustomValidity(''));
    }
}

// ==========================================================================
// Multi-Language Audio Advisory (SpeechSynthesis API)
// ==========================================================================
let currentUtterance = null;
let currentActiveButton = null;

function getSpeechLang(langCode) {
    return { en: 'en-IN', hi: 'hi-IN', kn: 'kn-IN' }[langCode] || (CFG.speechLang || 'en-IN');
}

function findBestVoice(langCode) {
    if (!('speechSynthesis' in window)) return null;

    const voices = window.speechSynthesis.getVoices() || [];
    const exact = getSpeechLang(langCode).toLowerCase();
    const base = exact.split('-')[0];

    const matching = voices.filter(v => (v.lang || '').toLowerCase().startsWith(base));
    if (!matching.length) return null;

    // Prefer a local voice (faster, often clearer) and an exact locale match.
    return matching.find(v => v.localService && (v.lang || '').toLowerCase() === exact)
        || matching.find(v => v.localService)
        || matching.find(v => (v.lang || '').toLowerCase() === exact)
        || matching[0];
}

function speakText(text, langCode, options = {}) {
    if (!('speechSynthesis' in window)) {
        alert(CFG.i18n?.ttsNotSupported || 'Speech output is not supported in your browser.');
        return null;
    }
    if (!text || !text.trim()) return null;

    const synth = window.speechSynthesis;
    synth.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = getSpeechLang(langCode);
    utterance.rate = options.rate || 0.92;
    utterance.pitch = options.pitch || 1.0;
    utterance.volume = 1.0;

    const voice = findBestVoice(langCode);
    if (voice) utterance.voice = voice;

    utterance.onend = () => {
        if (typeof options.onEnd === 'function') options.onEnd();
    };
    utterance.onerror = () => {
        if (typeof options.onEnd === 'function') options.onEnd();
    };

    currentUtterance = utterance;
    synth.speak(utterance);
    return utterance;
}

function playVoice(langCode) {
    if (!('speechSynthesis' in window)) {
        alert(CFG.i18n?.ttsNotSupported || 'Speech output is not supported in your browser.');
        return;
    }

    const synth = window.speechSynthesis;
    const existingButton = document.querySelector(`[data-voice-lang="${langCode}"]`);

    // If already speaking the same language, stop it.
    if (synth.speaking && currentActiveButton && currentActiveButton === existingButton) {
        synth.cancel();
        resetVoiceButtons();
        return;
    }

    synth.cancel();
    resetVoiceButtons();

    const scriptIds = { en: 'voiceScriptEn', hi: 'voiceScriptHi', kn: 'voiceScriptKn' };
    const scriptElement = document.getElementById(scriptIds[langCode]);
    const textScript = scriptElement ? scriptElement.textContent : '';

    if (!textScript || !textScript.trim()) {
        alert(CFG.i18n?.help || 'Audio prescription is not available for this language.');
        return;
    }

    if (existingButton) {
        existingButton.classList.add('speaking');
        currentActiveButton = existingButton;
    }

    speakText(textScript, langCode, { onEnd: resetVoiceButtons });
}

function resetVoiceButtons() {
    document.querySelectorAll('[data-voice-lang]').forEach(btn => {
        btn.classList.remove('speaking');
    });
    currentActiveButton = null;
}

// Voice may load asynchronously in Chrome.
if ('speechSynthesis' in window) {
    window.speechSynthesis.onvoiceschanged = () => {};
}

// Expose helpers to voice.js
window.playVoice = playVoice;
window.speakText = speakText;
