const form = document.querySelector('#analyze-form');
const fileInput = document.querySelector('#resume-file');
const dropzone = document.querySelector('#dropzone');
const filePreview = document.querySelector('#file-preview');
const jobDescription = document.querySelector('#job-description');
const analyzeButton = document.querySelector('#analyze-button');
const formError = document.querySelector('#form-error');
const results = document.querySelector('#results');

function showFile(file) {
  if (!file) return;
  const extension = file.name.split('.').pop().toUpperCase();
  if (!['PDF', 'DOCX'].includes(extension)) {
    formError.textContent = 'Please choose a PDF or DOCX file.';
    fileInput.value = '';
    return;
  }
  if (file.size > 8 * 1024 * 1024) {
    formError.textContent = 'The resume must be smaller than 8 MB.';
    fileInput.value = '';
    return;
  }
  formError.textContent = '';
  document.querySelector('#file-type').textContent = extension;
  document.querySelector('#file-name').textContent = file.name;
  document.querySelector('#file-size').textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB · Ready to analyze`;
  dropzone.hidden = true;
  filePreview.hidden = false;
}

fileInput.addEventListener('change', () => showFile(fileInput.files[0]));
['dragenter', 'dragover'].forEach(event => dropzone.addEventListener(event, e => { e.preventDefault(); dropzone.classList.add('dragging'); }));
['dragleave', 'drop'].forEach(event => dropzone.addEventListener(event, e => { e.preventDefault(); dropzone.classList.remove('dragging'); }));
dropzone.addEventListener('drop', event => {
  const file = event.dataTransfer.files[0];
  const transfer = new DataTransfer();
  transfer.items.add(file);
  fileInput.files = transfer.files;
  showFile(file);
});
document.querySelector('#remove-file').addEventListener('click', () => {
  fileInput.value = '';
  filePreview.hidden = true;
  dropzone.hidden = false;
});

jobDescription.addEventListener('input', () => {
  const words = jobDescription.value.trim() ? jobDescription.value.trim().split(/\s+/).length : 0;
  document.querySelector('#word-count').textContent = words;
});

form.addEventListener('submit', async event => {
  event.preventDefault();
  formError.textContent = '';
  if (!fileInput.files[0]) return formError.textContent = 'Upload a resume to continue.';
  if (jobDescription.value.trim().length < 80) return formError.textContent = 'Paste a more complete job description (at least 80 characters).';

  analyzeButton.classList.add('loading');
  analyzeButton.disabled = true;
  try {
    const response = await fetch('/api/analyze', { method: 'POST', body: new FormData(form) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Analysis failed.');
    renderResults(data);
  } catch (error) {
    formError.textContent = error.message;
  } finally {
    analyzeButton.classList.remove('loading');
    analyzeButton.disabled = false;
  }
});

function renderResults(data) {
  document.querySelector('#result-filename').textContent = data.file_name;
  animateNumber(document.querySelector('#match-score'), data.match_score);
  document.querySelector('#score-ring').style.setProperty('--score', `${data.match_score * 3.6}deg`);
  document.querySelector('#verdict-title').textContent = data.verdict.title;
  document.querySelector('#verdict-message').textContent = data.verdict.message;
  document.querySelector('#ranking-tier').textContent = data.ranking.tier;
  document.querySelector('#ranking-label').textContent = data.ranking.label;
  document.querySelector('#ranking-percentile').textContent = data.ranking.percentile;
  document.querySelector('#matched-count').textContent = data.stats.matched;
  document.querySelector('#coverage-count').textContent = data.stats.required ? `${Math.round(data.stats.matched / data.stats.required * 100)}%` : '—';
  document.querySelector('#resume-words').textContent = data.stats.resume_words;
  document.querySelector('#result-summary').textContent = data.summary;
  document.querySelector('#verdict-banner-title').textContent = data.verdict.title;
  document.querySelector('#matched-badge').textContent = data.matched_skills.length;
  document.querySelector('#missing-badge').textContent = data.missing_skills.length;
  document.querySelector('#disclaimer').textContent = data.disclaimer;

  document.querySelector('#score-breakdown').innerHTML = data.score_breakdown.map(item => `
    <div class="breakdown-item">
      <div class="breakdown-copy"><div><strong>${escapeHtml(item.label)}</strong><small>${escapeHtml(item.description)}</small></div><span class="breakdown-score">${item.score} / ${item.max}</span></div>
      <div class="track"><span style="width:${item.score / item.max * 100}%"></span></div>
    </div>`).join('');

  renderSkills('#matched-skills', data.matched_skills, 'No explicit required skills were found in both documents.');
  renderSkills('#missing-skills', data.missing_skills, 'No major skill gaps detected.');
  document.querySelector('#suggestions-list').innerHTML = data.suggestions.map((item, index) => `
    <div class="suggestion"><span class="suggestion-index">${String(index + 1).padStart(2, '0')}</span><div><h4>${escapeHtml(item.title)}</h4><p>${escapeHtml(item.detail)}</p><span class="priority">${escapeHtml(item.priority)} priority</span></div></div>`).join('');

  results.hidden = false;
  results.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function renderSkills(selector, skills, emptyMessage) {
  document.querySelector(selector).innerHTML = skills.length
    ? skills.map(skill => `<span class="skill-chip">${escapeHtml(skill.name)}<small>${escapeHtml(skill.category)}</small></span>`).join('')
    : `<span class="empty-skills">${emptyMessage}</span>`;
}

function animateNumber(element, target) {
  const start = performance.now();
  function frame(now) {
    const progress = Math.min((now - start) / 900, 1);
    element.textContent = Math.round(target * (1 - Math.pow(1 - progress, 3)));
    if (progress < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
}

document.querySelector('#new-analysis').addEventListener('click', () => {
  results.hidden = true;
  form.reset();
  filePreview.hidden = true;
  dropzone.hidden = false;
  document.querySelector('#word-count').textContent = '0';
  document.querySelector('#analyzer').scrollIntoView({ behavior: 'smooth' });
});

