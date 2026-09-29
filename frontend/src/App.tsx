import './styles.css';

const metrics = [
  { label: 'Total Projects', value: '24' },
  { label: 'Total Scans', value: '128' },
  { label: 'Open Vulnerabilities', value: '19' },
  { label: 'Critical Findings', value: '4' },
];

const findings = [
  { severity: 'CRITICAL', rule: 'hardcoded secret', file: 'config.yaml', status: 'open' },
  { severity: 'HIGH', rule: 'outdated dependency', file: 'package.json', status: 'review' },
  { severity: 'MEDIUM', rule: 'weak cipher', file: 'crypto/util.py', status: 'open' },
];

export default function App() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <h1>SecureDevOpsHub</h1>
          <p>Developer security platform</p>
        </div>
        <button className="primary-btn">Trigger scan</button>
      </header>

      <section className="metrics-grid">
        {metrics.map((metric) => (
          <div key={metric.label} className="metric-card">
            <span>{metric.label}</span>
            <strong>{metric.value}</strong>
          </div>
        ))}
      </section>

      <section className="content-grid">
        <div className="panel">
          <h2>Recent findings</h2>
          <ul className="finding-list">
            {findings.map((item) => (
              <li key={`${item.file}-${item.rule}`}>
                <span className={`badge ${item.severity.toLowerCase()}`}>{item.severity}</span>
                <div>
                  <strong>{item.rule}</strong>
                  <small>{item.file}</small>
                </div>
                <span className="status">{item.status}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="panel">
          <h2>Project overview</h2>
          <div className="chart-bars">
            <div className="bar low" style={{ height: '55%' }} />
            <div className="bar medium" style={{ height: '70%' }} />
            <div className="bar high" style={{ height: '45%' }} />
            <div className="bar critical" style={{ height: '25%' }} />
          </div>
          <div className="legend">
            <span><i className="dot low" /> Low</span>
            <span><i className="dot medium" /> Medium</span>
            <span><i className="dot high" /> High</span>
            <span><i className="dot critical" /> Critical</span>
          </div>
        </div>
      </section>
    </div>
  );
}
