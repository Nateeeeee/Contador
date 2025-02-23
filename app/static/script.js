function atualizarContador() {
  const dataInicial = new Date("2025-02-10T00:00:00").getTime();
  const agora = new Date().getTime();
  const diferenca = agora - dataInicial;

  if (diferenca < 0) {
    document.getElementById("contador").innerHTML = "A data ainda não chegou.";
    return;
  }

  const dias = Math.floor(diferenca / (1000 * 60 * 60 * 24));
  const horas = Math.floor((diferenca % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutos = Math.floor((diferenca % (1000 * 60 * 60)) / (1000 * 60));
  const segundos = Math.floor((diferenca % (1000 * 60)) / 1000);

  document.getElementById("contador").innerHTML = 
    `${dias}d ${horas}h ${minutos}m ${segundos}s`;
}

setInterval(atualizarContador, 1000);
atualizarContador();