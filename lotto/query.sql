select *
from Lotto
where (no1, no2, no3, no4, no5, no6) = (select no1, no2, no3, no4, no5, no6 from mylotto)

select * from MyLotto;
delete from MyLotto;
commit;