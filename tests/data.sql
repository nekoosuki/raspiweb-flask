INSERT INTO user (devname, password, isadmin)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',0),
  ('testadmin', 'pbkdf2:sha256:150000$lqO10DIs$6f25a819da1195a383d1c0aa932353efe5ae61708b3acd2892d71cbf900c065b',1),
  ('other', 'pbkdf2:sha256:150000$u453Vtef$c1585904025e989ef14fcc92dcdb07c31156a901195274dddedda83368a50e1c',0);

INSERT INTO config (devname)
VALUES
('test'),
('testadmin');

INSERT INTO config (devname, conf, iou)
VALUES
('other', 0.5, 0.5);