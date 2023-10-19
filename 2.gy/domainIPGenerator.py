import struct

packer = struct.Struct('20s i')

datas = [
(b"inf.elte.hu",21),
(b"elte.hu",22),
(b"to.ttk.elte.hu",25),
(b"ggombos.web.elte.hu",42),
(b"lakis.web.elte.hu",80),
(b"tms.inf.elte.hu",88),
(b"canvas.elte.hu",443),
(b"neptun.elte.hu",22),
(b"szalaigj.web.elte.hu",80),
(b"icephoenix.web.elte.hu",80),
]

with open('domainPort.bin', 'wb') as f:
	for v in datas:
		packed_data = packer.pack(*v)
		f.write(packed_data)