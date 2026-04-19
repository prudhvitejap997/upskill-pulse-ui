/* ─────────────────────────────────────────────
   QuizCraft — UI Logic
   Backend integration points marked with:  [API]
───────────────────────────────────────────── */

// ── State ──────────────────────────────────
const state = {
  files:       [],
  topic:       '',
  difficulty:  'medium',
  questionCount: 10,
  questions:   [],
  answers:     {},   // { qIndex: selectedOptionIndex }
  currentQ:    0,
  timerSec:    0,
  timerHandle: null,
  startTime:   null,
};

// ── DOM Refs ───────────────────────────────
const $ = id => document.getElementById(id);
const screens = {
  setup:    $('screen-setup'),
  loading:  $('screen-loading'),
  quiz:     $('screen-quiz'),
  results:  $('screen-results'),
};

// ── Screen switcher ────────────────────────
function showScreen(name) {
  Object.values(screens).forEach(s => s.classList.remove('active'));
  screens[name].classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ══════════════════════════════════════════
//  SCREEN 1 — SETUP
// ══════════════════════════════════════════

// File upload
const dropzone  = $('dropzone');
const fileInput = $('file-input');
const fileList  = $('file-list');
const fileError = $('file-error');

dropzone.addEventListener('click', () => fileInput.click());

dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('drag-over'); });
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('drag-over'));
dropzone.addEventListener('drop', e => {
  e.preventDefault();
  dropzone.classList.remove('drag-over');
  handleFiles([...e.dataTransfer.files]);
});

fileInput.addEventListener('change', () => handleFiles([...fileInput.files]));

function handleFiles(incoming) {
  const allowed = ['application/pdf', 'text/plain'];
  const validExts = ['.pdf', '.txt'];
  fileError.classList.add('hidden');

  for (const f of incoming) {
    const ext = f.name.slice(f.name.lastIndexOf('.')).toLowerCase();
    if (!validExts.includes(ext)) {
      showFileError(`"${f.name}" is not a PDF or TXT file.`); continue;
    }
    if (state.files.length >= 5) {
      showFileError('Maximum 5 files allowed.'); break;
    }
    if (state.files.find(x => x.name === f.name)) continue; // skip duplicates
    state.files.push(f);
  }

  renderFileList();
  fileInput.value = '';
}

function showFileError(msg) {
  fileError.textContent = msg;
  fileError.classList.remove('hidden');
}

function renderFileList() {
  fileList.innerHTML = '';
  state.files.forEach((f, i) => {
    const ext  = f.name.slice(f.name.lastIndexOf('.')).toLowerCase();
    const icon = ext === '.pdf' ? '📕' : '📄';
    const size = f.size < 1024 ? `${f.size} B`
               : f.size < 1048576 ? `${(f.size/1024).toFixed(1)} KB`
               : `${(f.size/1048576).toFixed(1)} MB`;
    const li = document.createElement('li');
    li.className = 'file-item';
    li.innerHTML = `
      <span class="file-icon">${icon}</span>
      <span class="file-name">${f.name}</span>
      <span class="file-size">${size}</span>
      <button class="file-remove" title="Remove" data-idx="${i}">✕</button>
    `;
    fileList.appendChild(li);
  });

  fileList.querySelectorAll('.file-remove').forEach(btn => {
    btn.addEventListener('click', () => {
      state.files.splice(parseInt(btn.dataset.idx), 1);
      renderFileList();
    });
  });
}

// Stepper
const qDisplay = $('q-display');
const qCount   = $('q-count');

$('q-dec').addEventListener('click', () => {
  const v = Math.max(5, parseInt(qCount.value) - 5);
  qCount.value = v; qDisplay.textContent = v;
});
$('q-inc').addEventListener('click', () => {
  const v = Math.min(30, parseInt(qCount.value) + 5);
  qCount.value = v; qDisplay.textContent = v;
});

// Difficulty watch
document.querySelectorAll('input[name="difficulty"]').forEach(r => {
  r.addEventListener('change', () => { state.difficulty = r.value; });
});

// Generate
$('btn-generate').addEventListener('click', async () => {
  const topic = $('topic-input').value.trim();
  if (!topic) { $('topic-input').focus(); return; }

  state.topic        = topic;
  state.difficulty   = document.querySelector('input[name="difficulty"]:checked').value;
  state.questionCount = parseInt(qCount.value);
  state.answers      = {};
  state.currentQ     = 0;

  showScreen('loading');
  await runLoadingAnimation();
  await generateQuiz();
});

// ══════════════════════════════════════════
//  SCREEN 2 — LOADING ANIMATION
// ══════════════════════════════════════════
async function runLoadingAnimation() {
  const steps = ['ls1', 'ls2', 'ls3', 'ls4'];
  const msgs  = [
    'Extracting topics from your files…',
    'Analyzing content…',
    'Generating questions…',
    'Finalizing your quiz…'
  ];

  for (let i = 0; i < steps.length - 1; i++) {
    $('loading-status').textContent = msgs[i];
    $(steps[i]).classList.add('active');
    await delay(700);
    $(steps[i]).classList.remove('active');
    $(steps[i]).classList.add('done');
    $(steps[i]).textContent = '✔ ' + $(steps[i]).textContent.replace(/^📄|🧠|✍️|✅\s*/, '').trim();
  }
}

// ══════════════════════════════════════════
//  [API] QUIZ GENERATION
//  Replace the mock below with your backend call.
// ══════════════════════════════════════════
async function generateQuiz() {
  try {
    /*
      [API] — Send to backend:
        POST /api/generate-quiz
        FormData: { topic, difficulty, questionCount, files[] }
      Expect back:
        { questions: [ { question, options: [], correct: 0, topic } ] }

      const formData = new FormData();
      formData.append('topic', state.topic);
      formData.append('difficulty', state.difficulty);
      formData.append('questionCount', state.questionCount);
      state.files.forEach(f => formData.append('files', f));

      const res  = await fetch('/api/generate-quiz', { method: 'POST', body: formData });
      const data = await res.json();
      state.questions = data.questions;
    */

    // ── MOCK DATA (remove when backend is ready) ──
    await delay(600);
    state.questions = generateMockQuestions(state.topic, state.difficulty, state.questionCount);
    // ──────────────────────────────────────────────

    $('loading-status').textContent = 'Quiz ready!';
    $('ls4').classList.add('done');
    await delay(400);

    startQuiz();
  } catch (err) {
    console.error(err);
    $('loading-status').textContent = 'Something went wrong. Please try again.';
  }
}

// ══════════════════════════════════════════
//  SCREEN 3 — QUIZ
// ══════════════════════════════════════════
function startQuiz() {
  showScreen('quiz');
  buildPalette();
  renderQuestion(0);
  startTimer();
}

function renderQuestion(idx) {
  state.currentQ = idx;
  const q   = state.questions[idx];
  const tot = state.questions.length;

  $('q-number').textContent = `Question ${idx + 1} of ${tot}`;
  $('q-text').textContent   = q.question;

  // Progress
  const pct = ((idx + 1) / tot) * 100;
  $('progress-fill').style.width = pct + '%';
  $('progress-text').textContent  = `${idx + 1} / ${tot}`;

  // Badges
  $('quiz-topic-badge').textContent = state.topic;
  const db = $('quiz-diff-badge');
  db.textContent = { easy: '🌱 Easy', medium: '🔥 Medium', hard: '💀 Hard' }[state.difficulty];
  db.className   = `quiz-diff-badge diff-badge-${state.difficulty}`;

  // Options
  const ol = $('options-list');
  ol.innerHTML = '';
  const labels = ['A', 'B', 'C', 'D'];

  q.options.forEach((opt, i) => {
    const li = document.createElement('li');
    li.className = 'option-item' + (state.answers[idx] === i ? ' selected' : '');
    li.innerHTML = `
      <span class="option-badge">${labels[i]}</span>
      <span>${opt}</span>
    `;
    li.addEventListener('click', () => selectOption(idx, i));
    ol.appendChild(li);
  });

  // Nav buttons
  $('btn-prev').disabled = idx === 0;
  $('btn-next').textContent = idx === tot - 1 ? 'Finish →' : 'Next →';

  updatePalette();
}

function selectOption(qIdx, optIdx) {
  state.answers[qIdx] = optIdx;
  renderQuestion(qIdx);
}

// Nav
$('btn-prev').addEventListener('click', () => {
  if (state.currentQ > 0) renderQuestion(state.currentQ - 1);
});

$('btn-next').addEventListener('click', () => {
  if (state.currentQ < state.questions.length - 1) {
    renderQuestion(state.currentQ + 1);
  } else {
    confirmSubmit();
  }
});

$('btn-submit-quiz').addEventListener('click', confirmSubmit);

function confirmSubmit() {
  const unanswered = state.questions.length - Object.keys(state.answers).length;
  if (unanswered > 0) {
    const ok = window.confirm(`You have ${unanswered} unanswered question${unanswered > 1 ? 's' : ''}. Submit anyway?`);
    if (!ok) return;
  }
  stopTimer();
  showResults();
}

// Palette
function buildPalette() {
  const palette = $('palette');
  palette.innerHTML = '';
  state.questions.forEach((_, i) => {
    const btn = document.createElement('button');
    btn.className   = 'palette-btn';
    btn.textContent = i + 1;
    btn.addEventListener('click', () => renderQuestion(i));
    palette.appendChild(btn);
  });
}

function updatePalette() {
  const btns = $('palette').querySelectorAll('.palette-btn');
  btns.forEach((btn, i) => {
    btn.className = 'palette-btn';
    if (state.answers[i] !== undefined) btn.classList.add('answered');
    if (i === state.currentQ)           btn.classList.add('current');
  });
}

// Timer
function startTimer() {
  state.timerSec   = 0;
  state.startTime  = Date.now();
  clearInterval(state.timerHandle);
  state.timerHandle = setInterval(() => {
    state.timerSec++;
    const m = String(Math.floor(state.timerSec / 60)).padStart(2, '0');
    const s = String(state.timerSec % 60).padStart(2, '0');
    $('timer-display').textContent = `${m}:${s}`;
  }, 1000);
}

function stopTimer() { clearInterval(state.timerHandle); }

// ══════════════════════════════════════════
//  SCREEN 4 — RESULTS
// ══════════════════════════════════════════
function showResults() {
  showScreen('results');

  const qs      = state.questions;
  const total   = qs.length;
  let correct   = 0;
  let wrong     = 0;
  let skipped   = 0;
  const weakTopics = new Set();

  qs.forEach((q, i) => {
    if (state.answers[i] === undefined) {
      skipped++;
      weakTopics.add(q.topic);
    } else if (state.answers[i] === q.correct) {
      correct++;
    } else {
      wrong++;
      weakTopics.add(q.topic);
    }
  });

  const pct = Math.round((correct / total) * 100);

  // Score circle
  $('score-pct').textContent = pct + '%';
  const circumference = 326.7;
  const offset = circumference - (pct / 100) * circumference;
  setTimeout(() => {
    $('score-arc').style.strokeDashoffset = offset;
    const color = pct >= 70 ? 'var(--green)' : pct >= 40 ? 'var(--yellow)' : 'var(--red)';
    $('score-arc').style.stroke = color;
    $('score-pct').style.color  = color;
  }, 100);

  // Stats
  $('stat-correct').textContent = correct;
  $('stat-wrong').textContent   = wrong;
  $('stat-skipped').textContent = skipped;

  // Grade
  const grade = getGrade(pct);
  $('grade-emoji').textContent   = grade.emoji;
  $('grade-title').textContent   = grade.title;
  $('grade-message').textContent = grade.message;
  $('grade-banner').style.borderColor = grade.color;

  // Topic feedback
  const chipContainer = $('topic-chips');
  chipContainer.innerHTML = '';
  if (weakTopics.size === 0) {
    chipContainer.innerHTML = `<span class="no-feedback">🎉 Great job! No weak areas detected.</span>`;
  } else {
    weakTopics.forEach(t => {
      const chip = document.createElement('span');
      chip.className   = 'topic-chip';
      chip.textContent = `📌 ${t}`;
      chipContainer.appendChild(chip);
    });
  }

  // Answer review
  const reviewList = $('review-list');
  reviewList.innerHTML = '';
  const labels = ['A', 'B', 'C', 'D'];

  qs.forEach((q, i) => {
    const userAns = state.answers[i];
    const isSkipped = userAns === undefined;
    const isCorrect = !isSkipped && userAns === q.correct;
    const status    = isSkipped ? 'skipped' : isCorrect ? 'correct' : 'wrong';
    const icon      = isSkipped ? '—' : isCorrect ? '✓' : '✗';

    const item = document.createElement('div');
    item.className = 'review-item';
    item.innerHTML = `
      <div class="review-item-header">
        <div class="review-status ${status}">${icon}</div>
        <div class="review-q"><strong>Q${i+1}.</strong> ${q.question}</div>
      </div>
      <div class="review-answers">
        <div class="ans-row">
          <span class="ans-label">Your answer:</span>
          <span class="ans-val ${isSkipped ? '' : isCorrect ? 'correct-ans' : 'wrong-ans'}">
            ${isSkipped ? '(not answered)' : `${labels[userAns]}. ${q.options[userAns]}`}
          </span>
        </div>
        ${!isCorrect ? `
        <div class="ans-row">
          <span class="ans-label">Correct answer:</span>
          <span class="ans-val correct-ans">${labels[q.correct]}. ${q.options[q.correct]}</span>
        </div>` : ''}
      </div>
    `;
    reviewList.appendChild(item);
  });
}

function getGrade(pct) {
  if (pct >= 90) return { emoji: '🏆', title: 'Outstanding!',    message: 'You nailed it. Exceptional performance!',         color: 'var(--green)'  };
  if (pct >= 75) return { emoji: '🎯', title: 'Great Job!',      message: 'Strong performance. A few areas to polish.',       color: 'var(--green)'  };
  if (pct >= 60) return { emoji: '👍', title: 'Good Effort!',    message: 'Decent score. Review the highlighted topics.',     color: 'var(--yellow)' };
  if (pct >= 40) return { emoji: '📖', title: 'Keep Studying!',  message: 'You need more practice on several topics.',        color: 'var(--yellow)' };
  return            { emoji: '💪', title: 'Don\'t Give Up!',     message: 'Revisit your study material and try again.',       color: 'var(--red)'    };
}

// ── Result action buttons ──
$('btn-retake').addEventListener('click', () => {
  state.answers  = {};
  state.currentQ = 0;
  startQuiz();
});

$('btn-new-quiz').addEventListener('click', () => {
  resetAll();
  showScreen('setup');
});

function resetAll() {
  state.files        = [];
  state.topic        = '';
  state.questions    = [];
  state.answers      = {};
  state.currentQ     = 0;
  stopTimer();
  renderFileList();
  $('topic-input').value   = '';
  $('q-count').value       = 10;
  $('q-display').textContent = 10;
  // Reset loading steps
  ['ls1','ls2','ls3','ls4'].forEach(id => {
    const el = $(id);
    el.classList.remove('active','done');
  });
  $('ls1').textContent = '📄 Reading files';
  $('ls2').textContent = '🧠 Analyzing content';
  $('ls3').textContent = '✍️ Generating questions';
  $('ls4').textContent = '✅ Almost done';
}

// ══════════════════════════════════════════
//  MOCK QUESTION GENERATOR
//  [API] Remove this entire block once backend is connected.
// ══════════════════════════════════════════
function generateMockQuestions(topic, difficulty, count) {
  const subtopics = [
    `${topic} — Fundamentals`,
    `${topic} — Core Concepts`,
    `${topic} — Advanced Topics`,
    `${topic} — Applications`,
    `${topic} — History & Context`,
  ];

  const templates = {
    easy: [
      { q: `What is the primary purpose of {topic}?`,           opts: ['To simplify complex tasks','To replace human effort','To store information','To process data'],           correct: 0 },
      { q: `Which of the following best defines {topic}?`,      opts: ['A set of rules','A framework','A systematic approach','All of the above'],                               correct: 3 },
      { q: `{topic} was first introduced in which era?`,        opts: ['Modern times','Ancient history','Industrial revolution','Digital age'],                                  correct: 0 },
      { q: `What is a common use case for {topic}?`,            opts: ['Education','Entertainment','Industry','All of the above'],                                              correct: 3 },
      { q: `Which term is most closely associated with {topic}?`,opts: ['Innovation','Tradition','Regression','Stagnation'],                                                    correct: 0 },
    ],
    medium: [
      { q: `How does {topic} differ from traditional approaches?`, opts: ['It uses automation','It requires less data','It is slower','It is more expensive'],                  correct: 0 },
      { q: `What is a key challenge in implementing {topic}?`,    opts: ['Lack of data','Resistance to change','Technical complexity','All of the above'],                      correct: 3 },
      { q: `Which methodology is most aligned with {topic}?`,    opts: ['Agile','Waterfall','Spiral','RAD'],                                                                    correct: 0 },
      { q: `In the context of {topic}, what does optimization mean?`,opts: ['Maximizing output','Reducing errors','Improving efficiency','All of the above'],                   correct: 3 },
      { q: `What role does feedback play in {topic}?`,           opts: ['Critical for improvement','Irrelevant','Slows progress','Causes confusion'],                           correct: 0 },
    ],
    hard: [
      { q: `Critically evaluate the trade-off between accuracy and efficiency in {topic}.`, opts: ['Accuracy is always prioritized','Efficiency trumps accuracy','Both are equally important depending on context','Neither matters'], correct: 2 },
      { q: `Which theoretical framework best underpins {topic}?`, opts: ['Systems theory','Chaos theory','Information theory','All depending on context'],                     correct: 3 },
      { q: `What is the most significant limitation of current {topic} implementations?`, opts: ['Scalability','Interpretability','Computational cost','All of the above'],    correct: 3 },
      { q: `How would you assess the ethical implications of {topic} in society?`,        opts: ['Net positive','Net negative','Context-dependent','Not applicable'],            correct: 2 },
      { q: `Which of the following represents the cutting edge of {topic} research?`,     opts: ['Foundation models','Rule-based systems','Expert systems','Decision trees'],   correct: 0 },
    ],
  };

  const pool = templates[difficulty];
  const questions = [];

  for (let i = 0; i < count; i++) {
    const tmpl    = pool[i % pool.length];
    const subTopic = subtopics[i % subtopics.length];
    questions.push({
      question: tmpl.q.replace(/{topic}/g, topic),
      options:  tmpl.opts,
      correct:  tmpl.correct,
      topic:    subTopic,
    });
  }

  return questions;
}

// ── Utility ────────────────────────────────
const delay = ms => new Promise(r => setTimeout(r, ms));
