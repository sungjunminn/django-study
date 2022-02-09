var ppl_pie = document.getElementById('pplPieChart').getContext('2d');
var pplPieChart = new Chart(ppl_pie, {
  type: 'pie',
  data: {
    labels: ['male', 'female'],
    datasets: [{
      data: pie_chart_ppl,
      backgroundColor: [
        "#f7323f",
        "#673ba7"
        ],
        borderWidth: 0
      }]
    }
  });