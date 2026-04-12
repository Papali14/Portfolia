const EXPECTED_RETURNS = { equity: 0.12, debt: 0.07, gold: 0.06, cash: 0.04 };
const BASE_RISK_ALLOCATIONS = {
  conservative: { equity: 0.25, debt: 0.55, gold: 0.10, cash: 0.10 },
  moderate: { equity: 0.45, debt: 0.35, gold: 0.10, cash: 0.10 },
  growth: { equity: 0.60, debt: 0.25, gold: 0.10, cash: 0.05 },
  aggressive: { equity: 0.75, debt: 0.15, gold: 0.05, cash: 0.05 }
};

const mockPanHoldings = [
  { symbol: "NIFTYBEES", asset_class: "equity", market_value: 350000 },
  { symbol: "GILT-FUND", asset_class: "debt", market_value: 180000 },
  { symbol: "GOLDBEES", asset_class: "gold", market_value: 80000 },
  { symbol: "SAVINGS", asset_class: "cash", market_value: 40000 }
];

const sourceRadios = document.querySelectorAll('input[name="source"]');
const fileSource = document.getElementById('fileSource');
const panSource = document.getElementById('panSource');

sourceRadios.forEach(r => r.addEventListener('change', () => {
  const source = document.querySelector('input[name="source"]:checked').value;
  fileSource.classList.toggle('hidden', source !== 'file');
  panSource.classList.toggle('hidden', source !== 'pan');
}));

document.getElementById('runBtn').addEventListener('click', async () => {
  const error = document.getElementById('error');
  error.textContent = '';
  try {
    const holdings = await getHoldings();
    const recommendation = runStrategy(holdings, {
      target: parseFloat(document.getElementById('target').value),
      years: parseInt(document.getElementById('years').value, 10),
      risk: document.getElementById('risk').value,
      monthly: parseFloat(document.getElementById('monthly').value)
    });
    renderResult(recommendation);
  } catch (e) {
    document.getElementById('result').classList.add('hidden');
    error.textContent = e.message;
  }
});

async function getHoldings() {
  const source = document.querySelector('input[name="source"]:checked').value;
  if (source === 'pan') {
    const pan = document.getElementById('pan').value.trim().toUpperCase();
    if (pan.length !== 10) throw new Error('PAN must be 10 characters.');
    return mockPanHoldings;
  }

  const file = document.getElementById('csvFile').files[0];
  if (!file) throw new Error('Please upload a CSV file.');
  const text = await file.text();
  return parseCsv(text);
}

function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/);
  const headers = lines[0].split(',').map(s => s.trim());
  const required = ['symbol', 'asset_class', 'market_value'];
  if (!required.every(h => headers.includes(h))) throw new Error('CSV headers missing required fields.');
  return lines.slice(1).map(line => {
    const cols = line.split(',');
    const row = Object.fromEntries(headers.map((h, i) => [h, (cols[i] || '').trim()]));
    const asset = row.asset_class.toLowerCase();
    if (!['equity', 'debt', 'gold', 'cash'].includes(asset)) throw new Error(`Invalid asset class: ${asset}`);
    return { symbol: row.symbol, asset_class: asset, market_value: Number(row.market_value) };
  });
}

function runStrategy(holdings, goal) {
  const total = holdings.reduce((s, h) => s + h.market_value, 0);
  if (!total) throw new Error('Portfolio value must be positive.');
  const current = { equity: 0, debt: 0, gold: 0, cash: 0 };
  holdings.forEach(h => current[h.asset_class] += h.market_value);
  Object.keys(current).forEach(k => current[k] /= total);

  const target = { ...BASE_RISK_ALLOCATIONS[goal.risk] };
  if (goal.years <= 3) { target.equity -= 0.15; target.debt += 0.15; }
  else if (goal.years <= 7) { target.equity -= 0.08; target.debt += 0.08; }

  const rebalance = {};
  const gaps = {};
  let gapSum = 0;
  for (const asset of Object.keys(target)) {
    rebalance[asset] = (target[asset] - current[asset]) * total;
    gaps[asset] = Math.max(0, target[asset] - current[asset]);
    gapSum += gaps[asset];
  }

  const sip = {};
  for (const asset of Object.keys(target)) {
    sip[asset] = gapSum === 0 ? target[asset] : gaps[asset] / gapSum;
  }

  const annualReturn = Object.keys(target).reduce((s, a) => s + target[a] * EXPECTED_RETURNS[a], 0);
  const monthlyRate = annualReturn / 12;
  const months = goal.years * 12;
  const fvLump = total * ((1 + monthlyRate) ** months);
  const fvSip = monthlyRate === 0 ? goal.monthly * months : goal.monthly * ((((1 + monthlyRate) ** months) - 1) / monthlyRate);
  const projected = fvLump + fvSip;

  return { total, current, target, rebalance, sip, annualReturn, projected, onTrack: projected >= goal.target };
}

function renderResult(r) {
  document.getElementById('result').classList.remove('hidden');
  document.getElementById('kpiCurrent').textContent = fmt(r.total);
  document.getElementById('kpiReturn').textContent = `${(r.annualReturn * 100).toFixed(2)}%`;
  document.getElementById('kpiProjected').textContent = fmt(r.projected);
  document.getElementById('kpiTrack').textContent = r.onTrack ? 'On track' : 'Needs action';

  const rows = document.getElementById('allocationRows');
  rows.innerHTML = '';
  ['equity', 'debt', 'gold', 'cash'].forEach(asset => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${asset}</td><td>${(r.current[asset] * 100).toFixed(2)}%</td><td>${(r.target[asset] * 100).toFixed(2)}%</td><td>${(r.sip[asset] * 100).toFixed(2)}%</td><td>${fmt(r.rebalance[asset])}</td>`;
    rows.appendChild(tr);
  });
}

function fmt(v) {
  return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(v);
}
