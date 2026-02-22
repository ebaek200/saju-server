function analyzeSaju(raw, isPaid) {

  const summary = `
연주 ${raw.year.stem}${raw.year.branch}
월주 ${raw.month.stem}${raw.month.branch}
일주 ${raw.day.stem}${raw.day.branch}
시주 ${raw.hour.stem}${raw.hour.branch}
`;

  if (!isPaid) {
    return { summary };
  }

  return {
    summary,
    detail: "유료 상세 해설 영역"
  };
}

module.exports = { analyzeSaju };