
-- depois de rodar o código da gabi, rodar esse script para puxar o nome/id do laboratório junto com a marca

-- por que?
-- na base_filtrada_subgrupos.csv o campo marca esta muito granular
-- o que implica na regressão, pois teremos muitos coeficientes (69) só de marcas
select a.*, b.nomeLaboratorio
from marca as a
inner join laboratorio as b
on a.laboratorio = b.idlaboratorio;