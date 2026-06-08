import { useEffect, useState } from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  Legend
} from 'recharts';
import { TagCloud } from 'react-tagcloud';
import { fetchMetric, askAi } from './api';
import ChartCard from './components/ChartCard';

const COLORS = ['#0c6ca8', '#f15a24', '#2d936c', '#ffc145', '#7b2cbf', '#ef476f'];

export default function App() {
  const [summary, setSummary] = useState(null);
  const [byDay, setByDay] = useState([]);
  const [bySource, setBySource] = useState([]);
  const [byCategory, setByCategory] = useState([]);
  const [byLanguage, setByLanguage] = useState([]);
  const [avgReading, setAvgReading] = useState([]);
  const [weekdayDist, setWeekdayDist] = useState([]);
  const [longReadRatio, setLongReadRatio] = useState([]);
  const [tagCloud, setTagCloud] = useState([]);
  const [question, setQuestion] = useState('How many articles were published this week?');
  const [answer, setAnswer] = useState('');

  useEffect(() => {
    async function load() {
      const [d0, d1, d2, d3, d4, d5, d6, d7, d8] = await Promise.all([
        fetchMetric('summary'),
        fetchMetric('articles-by-day'),
        fetchMetric('articles-by-source'),
        fetchMetric('articles-by-category'),
        fetchMetric('articles-by-language'),
        fetchMetric('avg-reading-time'),
        fetchMetric('weekday-distribution'),
        fetchMetric('long-read-ratio'),
        fetchMetric('tag-cloud')
      ]);
      setSummary(d0);
      setByDay(d1);
      setBySource(d2);
      setByCategory(d3);
      setByLanguage(d4);
      setAvgReading(d5);
      setWeekdayDist(d6);
      setLongReadRatio(d7);
      setTagCloud(d8.map((item) => ({ value: item.word, count: item.count })));
    }

    load().catch((err) => {
      console.error('Failed to load dashboard data', err);
    });
  }, []);

  async function handleAsk(event) {
    event.preventDefault();
    const res = await askAi(question);
    setAnswer(res.answer);
  }

  return (
    <div className="page">
      <header className="hero">
        <h1>Articles AI Analytics Dashboard</h1>
        <p>CSV -> PostgreSQL -> Analytics -> MindsDB Agent</p>
      </header>

      <main className="grid">
        {summary && (
          <section className="kpi-row">
            <div className="kpi"><span>Total Articles</span><strong>{summary.total_articles}</strong></div>
            <div className="kpi"><span>Sources</span><strong>{summary.total_sources}</strong></div>
            <div className="kpi"><span>Categories</span><strong>{summary.total_categories}</strong></div>
            <div className="kpi"><span>Avg Read Time</span><strong>{summary.avg_read_minutes} min</strong></div>
          </section>
        )}

        <ChartCard title="Articles Per Day">
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={byDay}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Legend />
              <Line dataKey="total" stroke="#0c6ca8" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Articles By Source">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={bySource}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="source" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="total" fill="#f15a24" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Articles By Category">
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={byCategory} dataKey="total" nameKey="category" outerRadius={95} label>
                {byCategory.map((entry, idx) => (
                  <Cell key={entry.category} fill={COLORS[idx % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Articles By Language">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={byLanguage}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="language" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="total" fill="#2d936c" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Average Reading Time By Source">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={avgReading}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="source" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="average_minutes" fill="#7b2cbf" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Weekday Distribution">
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={weekdayDist}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="weekday" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Line dataKey="total" stroke="#ef476f" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Long Read vs Short Read">
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={longReadRatio} dataKey="total" nameKey="bucket" outerRadius={95} label>
                {longReadRatio.map((entry, idx) => (
                  <Cell key={entry.bucket} fill={COLORS[idx % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Tag Cloud">
          <div className="tag-cloud-wrap">
            <TagCloud
              minSize={14}
              maxSize={38}
              tags={tagCloud}
              shuffle={false}
              className="tag-cloud"
            />
          </div>
        </ChartCard>
      </main>

      <section className="ai-box">
        <h2>Ask MindsDB Agent</h2>
        <form onSubmit={handleAsk}>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask about the articles dataset"
          />
          <button type="submit">Ask</button>
        </form>
        {answer && <p className="answer">{answer}</p>}
      </section>
    </div>
  );
}
