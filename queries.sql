-- quantos medicamentos temos por marcas??

select m.nomeMarca, COUNT(md.idMedicamentos) as total_medicamentos
from marca m
join medicamentos md on md.marca = m.idmarca
group by m.nomeMarca
order by total_medicamentos desc;

-- quais marcas são as mais caras??

select m.nomeMarca, avg(md.preco) as preco_medio
from medicamentos md
join marca m on md.marca = m.idmarca
group by m.nomeMarca
order by preco_medio desc;


