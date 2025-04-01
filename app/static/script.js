function atualizarContador() {
  const dataInicial = new Date("2025-02-10T00:00:00");
  const agora = new Date();

  if (agora < dataInicial) {
    document.getElementById("contador").innerHTML = "A data ainda não chegou.";
    return;
  }

  const diferenca = agora - dataInicial;

  const anos = agora.getFullYear() - dataInicial.getFullYear();
  const meses = (anos * 12) + (agora.getMonth() - dataInicial.getMonth());
  const dias = Math.floor(diferenca / (1000 * 60 * 60 * 24));
  const horas = Math.floor((diferenca % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutos = Math.floor((diferenca % (1000 * 60 * 60)) / (1000 * 60));
  const segundos = Math.floor((diferenca % (1000 * 60)) / 1000);

  document.getElementById("contador").innerHTML = 
    `${anos}a ${meses % 12}m ${dias}d ${horas}h ${minutos}m ${segundos}s`;
}

setInterval(atualizarContador, 1000);
atualizarContador();