INSERT INTO user (devname, password, isadmin)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',0),
  ('testadmin', 'pbkdf2:sha256:150000$lqO10DIs$6f25a819da1195a383d1c0aa932353efe5ae61708b3acd2892d71cbf900c065b',1);

INSERT INTO config (devname)
VALUES
('test')
