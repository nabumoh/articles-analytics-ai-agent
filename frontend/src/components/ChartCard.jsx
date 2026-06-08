export default function ChartCard({ title, children }) {
  return (
    <section className="card">
      <h3>{title}</h3>
      <div className="card-body">{children}</div>
    </section>
  );
}
