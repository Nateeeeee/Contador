function calcularDiferenca(dataInicial, dataFinal) {
  let anos = dataFinal.getFullYear() - dataInicial.getFullYear();
  let meses = dataFinal.getMonth() - dataInicial.getMonth();
  let dias = dataFinal.getDate() - dataInicial.getDate();

  if (dias < 0) {
      meses--;
      let ultimoDiaMesAnterior = new Date(dataFinal.getFullYear(), dataFinal.getMonth(), 0).getDate();
      dias += ultimoDiaMesAnterior;
  }

  if (meses < 0) {
      anos--;
      meses += 12;
  }

  return { anos, meses, dias };
}

function atualizarContador() {
  const dataInicial = new Date("2025-02-10T00:00:00");
  const agora = new Date();

  if (agora < dataInicial) {
      document.getElementById("contador").innerHTML = "A data ainda não chegou.";
      return;
  }

  const diferenca = calcularDiferenca(dataInicial, agora);
  const diferencaEmMilissegundos = agora - dataInicial;
  const horasTotais = Math.floor(diferencaEmMilissegundos / (1000 * 60 * 60));
  const minutos = Math.floor((diferencaEmMilissegundos % (1000 * 60 * 60)) / (1000 * 60));
  const segundos = Math.floor((diferencaEmMilissegundos % (1000 * 60)) / 1000);
  const horas = horasTotais % 24;

  let contadorTexto = `${diferenca.anos}A ${diferenca.meses}M ${diferenca.dias}d ${horas}h ${minutos}m ${segundos}s`;

  document.getElementById("contador").innerHTML = contadorTexto;
}

setInterval(atualizarContador, 1000);
atualizarContador();
