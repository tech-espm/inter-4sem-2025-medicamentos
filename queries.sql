-- quantos medicamentos temos por marcas??

select m.nomeMarca, COUNT(md.idMedicamentos) as total_medicamentos
from marca m
join medicamentos md on md.marca = m.idmarca
group by m.nomeMarca
order by total_medicamentos desc;

-- qual é o princípio ativo mais utilizado em medicamentos OTC?

