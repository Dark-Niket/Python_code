// Simple prediction window generator based on previous cycle start dates.
// Input: array of ISO date strings (older -> newer)
function predictWindow(cycleStartDates) {
  if (!Array.isArray(cycleStartDates) || cycleStartDates.length < 2) {
    return null;
  }
  const dates = cycleStartDates.map(d => new Date(d)).sort((a,b)=>a-b);
  const lengths = [];
  for (let i = 1; i < dates.length; i++) {
    const diffDays = Math.round((dates[i] - dates[i-1]) / (1000*3600*24));
    lengths.push(diffDays);
  }
  const avg = Math.round(lengths.reduce((a,b)=>a+b,0) / lengths.length);
  const variance = lengths.reduce((a,b)=>a + Math.pow(b - avg,2), 0) / lengths.length;
  const sd = Math.round(Math.sqrt(variance));
  const last = dates[dates.length - 1];
  const predicted = new Date(last);
  predicted.setDate(predicted.getDate() + avg);
  const windowPadding = Math.max(2, sd); // at least 2 days of padding
  const windowStart = new Date(predicted);
  windowStart.setDate(windowStart.getDate() - windowPadding);
  const windowEnd = new Date(predicted);
  windowEnd.setDate(windowEnd.getDate() + windowPadding);
  return {
    predictedStart: predicted.toISOString().slice(0,10),
    windowStart: windowStart.toISOString().slice(0,10),
    windowEnd: windowEnd.toISOString().slice(0,10),
    averageCycleLength: avg,
    sd
  };
}

module.exports = { predictWindow };
