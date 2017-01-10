#!/usr/bin/python2

from idc import *
from idaapi import *
from idautils import *

'''
Checks if the vtable is a possible sub-vtable.
'''

vtables = [ 0x1c74170, 0x1c74150, 0x1c74d90, 0x1c74d50, 0x15bae30, 0x15bae50, 0x15bae70, 0x15bae90, 0x15baeb0, 0x15e3650, 0x15e3690, 0x15e35d0, 0x15e3610, 0x15e48d0, 0x15e3770, 0x15e37b0, 0x15e3870, 0x15e38b0, 0x15e3a50, 0x15e3a10, 0x15e4ad0, 0x15e4b30, 0x15e4a70, 0x15e4c50, 0x15e4b90, 0x15e4cb0, 0x15e4690, 0x15e4bf0, 0x15e4d10, 0x15e4a10, 0x15e46f0, 0x15e50b0, 0x15e4d70, 0x15e5030, 0x15e4eb0, 0x15e4770, 0x15e4df0, 0x15e4f10, 0x15e4fd0, 0x15e4f70, 0x15e4e50, 0x15e4910, 0x15e4950, 0x15e4990, 0x15e49d0, 0x1d1c3d0, 0x1d1c430, 0x1d17bf0, 0x1d1c490, 0x1d1c4f0, 0x1d1c590, 0x1d1c5d0, 0x1d1c8b0, 0x1c741f0, 0x1d14910, 0x1d1c8f0, 0x1d1ca50, 0x1d1ca90, 0x1d1cad0, 0x1d1c9d0, 0x1d1ca10, 0x1d1ceb0, 0x1d1cef0, 0x1d1cf30, 0x1d1d0b0, 0x1d1d0f0, 0x1d1d130, 0x1d1d070, 0x1d1e790, 0x1d1e7b0, 0x1d1e7d0, 0x1d345b0, 0x1d34570, 0x1d14410, 0x1d14450, 0x1d15270, 0x1d152b0, 0x1d1adf0, 0x1d155b0, 0x1d155f0, 0x1d190b0, 0x1d15b50, 0x1d18710, 0x1d15b70, 0x1d29c30, 0x1d29b30, 0x1d29c70, 0x1d29b70, 0x1d29bb0, 0x1d29ab0, 0x1d29bf0, 0x1d29af0, 0x1d306b0, 0x1d306f0, 0x1d30770, 0x1d30730, 0x1d30630, 0x1d30670, 0x1d30270, 0x1d30290, 0x1d346f0, 0x1d34990, 0x1d35050, 0x1d35170, 0x1d34ad0, 0x1d350b0, 0x1d34ff0, 0x1d35110, 0x1d1e750, 0x1d355f0, 0x1d35630, 0x1d3ccf0, 0x1d3cd10, 0x1c749d0, 0x1c74830, 0x1c74b70, 0x1c76690, 0x1c7a150, 0x1c77590, 0x1c7c310, 0x1c7ae10, 0x1c76090, 0x1c76390, 0x1c784b0, 0x1c7bd10, 0x1c7a490, 0x1c7b110, 0x1c7a7d0, 0x1c77290, 0x1c7ab10, 0x1c787f0, 0x1c78190, 0x1c76c90, 0x1c7ba10, 0x1c78b30, 0x1c79b30, 0x1c78e70, 0x1c7c910, 0x1c76f90, 0x1c791b0, 0x1c7b710, 0x1c75d90, 0x1c7c610, 0x1c794f0, 0x1c77b90, 0x1c77e90, 0x1c7b410, 0x1c75a90, 0x1c79810, 0x1c77890, 0x1c76990, 0x1c79e50, 0x1c7c010, 0x1d14330, 0x1c74250, 0x1d14370, 0x1d14490, 0x1d1c390, 0x1d144d0, 0x1d3b470, 0x1d36c90, 0x1d36cd0, 0x1d3ae10, 0x1d3ae50, 0x1d3add0, 0x1d3afd0, 0x1d3afb0, 0x15b54d0, 0x15b5590, 0x15b5550, 0x15b5510, 0x15caad0, 0x15cab10, 0x15cab50, 0x15caa90, 0x15d4730, 0x15d46f0, 0x15a8d70, 0x15d4e90, 0x15f80f0, 0x15f9030, 0x15ed5b0, 0x15f4590, 0x15e3130, 0x15ec770, 0x15f5f30, 0x15eb070, 0x15e66f0, 0x15f4050, 0x15f4b50, 0x15fa370, 0x15eb190, 0x15ef070, 0x15f04d0, 0x15eab30, 0x15f8270, 0x15f2b10, 0x15efa10, 0x15f4f50, 0x15e5f90, 0x15ed550, 0x15f9e30, 0x15f2c30, 0x15ebe70, 0x15eb130, 0x15e7b50, 0x15e8f90, 0x15ec7d0, 0x15fa5b0, 0x15ef6f0, 0x15f4850, 0x15ef3d0, 0x15ec710, 0x15f46f0, 0x15ed4f0, 0x15f3e70, 0x15ec830, 0x15f4cb0, 0x15f43d0, 0x15ed610, 0x15ea730, 0x15ea2f0, 0x15e9eb0, 0x15f3710, 0x15f3950, 0x15eb0d0, 0x15e9a70, 0x15f32d0, 0x15e8410, 0x15f2e90, 0x15f8190, 0x15efd30, 0x15ee810, 0x15ebdb0, 0x15fa0b0, 0x15ee530, 0x15f7d90, 0x15f3a70, 0x15e6cd0, 0x15ed870, 0x15f1970, 0x15eecb0, 0x15f9f70, 0x15f3db0, 0x15f6850, 0x15ee210, 0x15f9a70, 0x15ee990, 0x15f91f0, 0x15e89b0, 0x15f9710, 0x15edef0, 0x15f3430, 0x15e57f0, 0x15f4210, 0x15edbd0, 0x15f9ed0, 0x15f9430, 0x15f8950, 0x15e5a90, 0x15e7370, 0x15fa430, 0x15f8bb0, 0x15f49f0, 0x15e5270, 0x15ebe10, 0x15e9550, 0x15f54b0, 0x15f0ad0, 0x15ebd50, 0x15e5d30, 0x15f30b0, 0x15f7eb0, 0x15f0d50, 0x15fa010, 0x15f1370, 0x15f3e10, 0x15e5550, 0x15e32d0, 0x15e31d0, 0x15e3250, 0x15e3210, 0x15e30b0, 0x15e3310, 0x15e3350, 0x15e3290, 0x15e3190, 0x1d29930, 0x1d19ef0, 0x15e3410, 0x15e3450, 0x15e3df0, 0x15e3d30, 0x15e3d90, 0x15e3cd0, 0x15fa210, 0x15fa250, 0x15fa290, 0x1d3c990, 0x1d3c9f0, 0x1d3c930, 0x1d3c650, 0x1d3ca50, 0x1d3be10, 0x1d3c190, 0x1d3be50, 0x1d3bf50, 0x1d3bf10, 0x1d3c250, 0x1d3be90, 0x1d3bed0, 0x1d3c210, 0x1d3c350, 0x1d3c390, 0x1d3bb10, 0x1d3c290, 0x1d3c3d0, 0x1d3c2d0, 0x1d3c150, 0x1d3c1d0, 0x1d3c310, 0x1d3bff0, 0x1d3c7b0, 0x1d3c8d0, 0x1d3c6f0, 0x1d3c810, 0x1d3c5f0, 0x1d3c750, 0x1d3c870, 0x1d3c030, 0x1d3c090, 0x1d3bf90, 0x1d3c0f0, 0x1d3bab0, 0x1d3caf0, 0x1d3c6b0, 0x1d3cab0, 0x1d3cdf0, 0x1d3ce30, 0x1d3cd30, 0x1d3cd70, 0x1d3ce70, 0x1d3cdb0, 0x1d3ccb0, 0x1d3b9b0, 0x1d3d790, 0x1d3d130, 0x1d3d8b0, 0x1d3d690, 0x1d3d590, 0x1d3d7f0, 0x1d3d910, 0x1d3d610, 0x1d3d510, 0x1d3d0d0, 0x1d3d850, 0x1d3d010, 0x1d3d9d0, 0x1d3da50, 0x1d3d3f0, 0x1d3d2f0, 0x1d3db30, 0x1d3d1f0, 0x1d1cdd0, 0x1c74eb0, 0x1d1ce30, 0x1c74ef0, 0x1c8edb0, 0x1c8ecf0, 0x1c8ec90, 0x1c8edf0, 0x1c8ee30, 0x1c8ee70, 0x1c74290, 0x1c8ec30, 0x1c8ed50, 0x1c96030, 0x1c95fb0, 0x1c96330, 0x1c96230, 0x1c96130, 0x1c962b0, 0x1c961b0, 0x1c960b0, 0x1c8eaf0, 0x1c96470, 0x1c96410, 0x1c96530, 0x1c8ebd0, 0x1c96590, 0x1c963b0, 0x1c964d0, 0x1c8eb70, 0x1ca2ab0, 0x1ca43b0, 0x1ca57f0, 0x1ca26f0, 0x1ca3b30, 0x1ca2af0, 0x1ca22b0, 0x1ca36f0, 0x1ca41f0, 0x1ca32b0, 0x1ca1a30, 0x1ca2e70, 0x1ca38b0, 0x1ca42b0, 0x1ca2a30, 0x1ca2b30, 0x1ca2330, 0x1ca52b0, 0x1ca4370, 0x1ca3a30, 0x1ca4e70, 0x1ca35f0, 0x1ca21b0, 0x1ca4a30, 0x1ca1d70, 0x1ca31b0, 0x1ca45f0, 0x1ca1930, 0x1ca5a30, 0x1ca2d70, 0x1ca3b70, 0x1ca41b0, 0x1ca14f0, 0x1ca55f0, 0x1ca2930, 0x1ca3d70, 0x1ca51b0, 0x1ca24f0, 0x1ca3930, 0x1ca4d70, 0x1ca20b0, 0x1ca34f0, 0x1ca4930, 0x1ca25f0, 0x1ca1c70, 0x1ca4bb0, 0x1ca30b0, 0x1ca2630, 0x1ca44f0, 0x1ca1830, 0x1ca5930, 0x1ca2c70, 0x1ca40b0, 0x1ca26b0, 0x1ca13f0, 0x1ca54f0, 0x1ca2830, 0x1ca3770, 0x1ca3c70, 0x1ca50b0, 0x1ca23f0, 0x1ca3830, 0x1ca4770, 0x1ca4c70, 0x1ca1fb0, 0x1ca47b0, 0x1ca33f0, 0x1ca47f0, 0x1ca36b0, 0x1ca4830, 0x1ca2170, 0x1ca4fb0, 0x1ca4f70, 0x1ca3730, 0x1ca4b70, 0x1ca1eb0, 0x1ca56f0, 0x1ca32f0, 0x1ca4730, 0x1ca29f0, 0x1ca1a70, 0x1ca2eb0, 0x1ca42f0, 0x1ca1630, 0x1ca5730, 0x1ca2a70, 0x1ca3eb0, 0x1ca11f0, 0x1ca52f0, 0x1ca2730, 0x1ca21f0, 0x1ca3630, 0x1ca5030, 0x1ca2b70, 0x1ca1db0, 0x1ca2bb0, 0x1ca31f0, 0x1ca4630, 0x1ca4bf0, 0x1ca1970, 0x1ca5770, 0x1ca2db0, 0x1ca4c30, 0x1ca1530, 0x1ca5630, 0x1ca2970, 0x1ca3db0, 0x1ca2770, 0x1ca51f0, 0x1ca2530, 0x1ca3970, 0x1ca4db0, 0x1ca1230, 0x1ca20f0, 0x1ca3530, 0x1ca4970, 0x1ca1cb0, 0x1ca30f0, 0x1ca4530, 0x1ca1870, 0x1ca2cb0, 0x1ca40f0, 0x1ca1430, 0x1ca5530, 0x1ca2870, 0x1ca3cb0, 0x1ca50f0, 0x1ca2430, 0x1ca3870, 0x1ca2ef0, 0x1ca1ff0, 0x1ca2f30, 0x1ca3430, 0x1ca4870, 0x1ca1bb0, 0x1ca2ff0, 0x1ca2fb0, 0x1ca4430, 0x1ca5870, 0x1ca4ff0, 0x1ca5830, 0x1ca3330, 0x1ca1170, 0x1ca22f0, 0x1ca11b0, 0x1ca4330, 0x1ca1670, 0x1ca3ef0, 0x1ca5330, 0x1ca2670, 0x1ca3ab0, 0x1ca4ef0, 0x1ca12b0, 0x1ca2230, 0x1ca3670, 0x1ca12f0, 0x1ca4ab0, 0x1ca1330, 0x1ca3230, 0x1ca4670, 0x1ca3370, 0x1ca19b0, 0x1ca2df0, 0x1ca1df0, 0x1ca33b0, 0x1ca4230, 0x1ca1570, 0x1ca5670, 0x1ca53f0, 0x1ca29b0, 0x1ca1130, 0x1ca5430, 0x1ca5230, 0x1ca2570, 0x1ca39b0, 0x1ca1370, 0x1ca2130, 0x1ca49b0, 0x1ca1cf0, 0x1ca3130, 0x1ca4570, 0x1ca18b0, 0x1ca3570, 0x1ca59b0, 0x1ca2cf0, 0x1ca4130, 0x1ca35b0, 0x1ca2f70, 0x1ca1470, 0x1ca5570, 0x1ca28b0, 0x1ca15f0, 0x1ca3cf0, 0x1ca4eb0, 0x1ca53b0, 0x1ca5130, 0x1ca2470, 0x1ca4cf0, 0x1ca1e70, 0x1ca2030, 0x1ca16b0, 0x1ca3470, 0x1ca48b0, 0x1ca16f0, 0x1ca3df0, 0x1ca1bf0, 0x1ca3030, 0x1ca1730, 0x1ca4470, 0x1ca17b0, 0x1ca58b0, 0x1ca1770, 0x1ca2bf0, 0x1ca43f0, 0x1ca4030, 0x1ca37b0, 0x1ca5470, 0x1ca27b0, 0x1ca2370, 0x1ca4cb0, 0x1ca57b0, 0x1ca5970, 0x1ca4df0, 0x1ca3f30, 0x1ca1270, 0x1ca5370, 0x1ca19f0, 0x1ca3af0, 0x1ca4f30, 0x1ca2270, 0x1ca4af0, 0x1ca1e30, 0x1ca1ab0, 0x1ca3270, 0x1ca46b0, 0x1ca1af0, 0x1ca2e30, 0x1ca1b30, 0x1ca4270, 0x1ca15b0, 0x1ca56b0, 0x1ca1c30, 0x1ca1b70, 0x1ca3e30, 0x1ca3bb0, 0x1ca25b0, 0x1ca3bf0, 0x1ca39f0, 0x1ca4e30, 0x1ca49f0, 0x1ca4a70, 0x1ca4b30, 0x1ca1d30, 0x1ca1f70, 0x1ca3170, 0x1ca45b0, 0x1ca18f0, 0x1ca59f0, 0x1ca2d30, 0x1ca3d30, 0x1ca4170, 0x1ca5270, 0x1ca14b0, 0x1ca55b0, 0x1ca28f0, 0x1ca5170, 0x1ca24b0, 0x1ca38f0, 0x1ca4d30, 0x1ca2070, 0x1ca34b0, 0x1ca46f0, 0x1ca48f0, 0x1ca3e70, 0x1ca3a70, 0x1ca3070, 0x1ca44b0, 0x1ca17f0, 0x1ca58f0, 0x1ca1ef0, 0x1ca0190, 0x1ca2c30, 0x1ca4070, 0x1ca1f30, 0x1ca13b0, 0x1ca54b0, 0x1ca27f0, 0x1ca3f70, 0x1ca3c30, 0x1ca5070, 0x1ca3fb0, 0x1ca23b0, 0x1ca37f0, 0x1ca3ff0, 0x1d15770, 0x1ca6630, 0x1d156b0, 0x1d157d0, 0x1d15710, 0x1ca65f0, 0x1cbc610, 0x1d13ed0, 0x1d13ff0, 0x1cd0890, 0x1d13f30, 0x1cc32b0, 0x1d14050, 0x1cd08f0, 0x1c75970, 0x1cd0950, 0x1cd09b0, 0x1c759d0, 0x1c75a30, 0x1cc3310, 0x1d13f90, 0x1cce790, 0x1cc37b0, 0x1cc38b0, 0x1cc3770, 0x1cc3830, 0x1cc3730, 0x1ccffb0, 0x1cc3870, 0x1cd0510, 0x1d17310, 0x1cc76b0, 0x1d17350, 0x1cc3270, 0x1ccf330, 0x1ccaa30, 0x1ccde70, 0x1ccddb0, 0x1ccddf0, 0x1ccde30, 0x1cc33d0, 0x1cc3450, 0x1cc3410, 0x1cce3f8, 0x1cce438, 0x1cce4a8, 0x1cce4f0, 0x1cce518, 0x1cce558, 0x1cce5c8, 0x1cc3370, 0x1cce470, 0x1cce590, 0x1cc3390, 0x1cc38f0, 0x1cce3d0, 0x1d141b0, 0x1d14190, 0x1d14870, 0x1d30c50, 0x1d148b0, 0x1d30c90, 0x1d14830, 0x1d1b1b0, 0x1d19710, 0x1d1b630, 0x1d1b930, 0x1d1b0b0, 0x1d1c0b0, 0x1d1b830, 0x1d1afb0, 0x1d1bfb0, 0x1d15630, 0x1d1b730, 0x1d1aeb0, 0x1d1beb0, 0x1d1bdb0, 0x1d1b530, 0x1d1bcb0, 0x1d1b430, 0x1d1bbb0, 0x1d1b330, 0x1d1bab0, 0x1d1b230, 0x1d1b9b0, 0x1d1b130, 0x1d1c130, 0x1d1b8b0, 0x1d1b030, 0x1d1c030, 0x1d1b7b0, 0x1d1af30, 0x1d1bf30, 0x1d1b6b0, 0x1d1ae30, 0x1d1be30, 0x1d1b5b0, 0x1d1bd30, 0x1d1b4b0, 0x1d1bc30, 0x1d1b3b0, 0x1d1bb30, 0x1d1b2b0, 0x1d1ba30, 0x1d1c2d0, 0x1d1c830, 0x1d1c310, 0x1d1d030, 0x1d15950, 0x1d15990, 0x1d15910, 0x1d14270, 0x15e30f0, 0x1d361f0, 0x1d159d0, 0x1d142b0, 0x1c7e350, 0x1c7e3d0, 0x1c7e2d0, 0x1cee050, 0x1cee230, 0x1cee190, 0x1cebd70, 0x1cee0f0, 0x1d19bb0, 0x1d19bf0, 0x1d19c30, 0x1cec030, 0x1cebff0, 0x1c747f0, 0x1d17e10, 0x1d17e50, 0x1d17e90, 0x1c74e30, 0x1d17ef0, 0x1c74df0, 0x1d18690, 0x1d186d0, 0x1d152f0, 0x1d151f0, 0x1d15350, 0x1d154c8, 0x1d15410, 0x1d153b0, 0x1d15470, 0x1d3cf30, 0x1d3cb50, 0x1d3ba30, 0x1d3cfb0, 0x1d3cf70, 0x1d20910, 0x1d0c1f0, 0x1cb6470, 0x1d30d10, 0x1cf1010, 0x1c86070, 0x1d204d0, 0x1d02090, 0x1d286d0, 0x1cbc0b0, 0x1c800d0, 0x1d22b30, 0x1cfddf0, 0x1d09950, 0x1cda130, 0x1d04990, 0x1d21090, 0x1cea170, 0x1c85bb0, 0x1cde3d0, 0x1d31490, 0x1d1f810, 0x1c90850, 0x1d20c50, 0x1d28e50, 0x1cb4050, 0x1cdb5b0, 0x1d20810, 0x1d20550, 0x1cef5b0, 0x1cd5730, 0x1d203d0, 0x1cf8bf0, 0x1cfa070, 0x1c88ff0, 0x1cd42b0, 0x1d06330, 0x1d22ff0, 0x1d34310, 0x1ce35d0, 0x1c81df0, 0x1cc9ff0, 0x1cec070, 0x1ce6910, 0x1c921f0, 0x1cbdad0, 0x1cf56b0, 0x1d20f90, 0x1cb97b0, 0x1c9e2d0, 0x1d25130, 0x1d20b50, 0x1cd70d0, 0x1c843f0, 0x1c95a70, 0x1cc1350, 0x1d34490, 0x1ccc410, 0x1cfa590, 0x1d20710, 0x1caca10, 0x1c85230, 0x1d07cd0, 0x1d11530, 0x1c7e450, 0x1cd7610, 0x1d202d0, 0x1cdab70, 0x1d10490, 0x1ce1710, 0x1c95550, 0x1cc6230, 0x1ce82b0, 0x1d0a330, 0x1c93b90, 0x1cbf470, 0x1c7de10, 0x1ca70d0, 0x1c97a70, 0x1cb0290, 0x1d212d0, 0x1d34390, 0x1c9fc70, 0x1ce4530, 0x1c8c550, 0x1c88670, 0x1d20e90, 0x1d0db90, 0x1d20290, 0x1cec570, 0x1c80588, 0x1caa4d0, 0x1cb4590, 0x1cfbf30, 0x1d20e50, 0x1d31950, 0x1d02ad0, 0x1c945d0, 0x1ca75f0, 0x1cdc510, 0x1d20610, 0x1ccbef0, 0x1ccfff0, 0x1cbf9d0, 0x1ce9c50, 0x1d0bcd0, 0x1d1ed90, 0x1cb5f50, 0x1ce2670, 0x1ca01d0, 0x1c99410, 0x1cac4d0, 0x1ca6690, 0x1cf05d0, 0x1cf86d0, 0x1cd3870, 0x1c848b0, 0x1ca06f0, 0x1d211d0, 0x1caaa30, 0x1cf4290, 0x1c93150, 0x1d293d0, 0x1d08710, 0x1d341d0, 0x1cfd8d0, 0x1d04470, 0x1c754b0, 0x1ca9f70, 0x1cc6750, 0x1d20d90, 0x1cddeb0, 0x1ccd890, 0x1cc8130, 0x1d28d50, 0x1c8a7b8, 0x1c90330, 0x1d242f0, 0x1ceb5f0, 0x1d0d670, 0x1ce2150, 0x1d0ff70, 0x1cb78f0, 0x1d20510, 0x1d335d0, 0x1d34350, 0x1cc7c10, 0x1d20cd0, 0x1cc1870, 0x1cc08d0, 0x1d210d0, 0x1cae8f0, 0x1d34190, 0x1d0cc30, 0x1ccc930, 0x1cc9ad0, 0x1cc4370, 0x1ce63f0, 0x1d20c90, 0x1cbd5b0, 0x1d28e90, 0x1cf5190, 0x1ced150, 0x1cfc970, 0x1cb9290, 0x1cae3d0, 0x1c8acf0, 0x1d344d0, 0x1c83f30, 0x1d20850, 0x1d129b0, 0x1d21c90, 0x1cd5c50, 0x1d34b30, 0x1cd6bb0, 0x1d20410, 0x1d26950, 0x1cc0e30, 0x1cbea30, 0x1cedb50, 0x1d00c10, 0x1ce4a50, 0x1cba710, 0x1d077b0, 0x1d11010, 0x1cda650, 0x1d32c50, 0x1c87370, 0x1ca8ad0, 0x1ce7d90, 0x1cbef50, 0x1d181d0, 0x1d20fd0, 0x1cf0af0, 0x1cbac30, 0x1cafd70, 0x1caba50, 0x1d20b90, 0x1ce2b90, 0x1cbb150, 0x1d20750, 0x1ce11f0, 0x1d025b0, 0x1c80f50, 0x1c7f750, 0x1d20310, 0x1d234b0, 0x1ca0c10, 0x1d26eb0, 0x1cdbff0, 0x1ccb9d0, 0x1d21150, 0x1c835b0, 0x1cabf70, 0x1ce9730, 0x1ce9210, 0x1d0b7b0, 0x1cc6c70, 0x1c7f290, 0x1d21310, 0x1cb1710, 0x1d34210, 0x1cd8cb0, 0x1d255f0, 0x1cb0cd0, 0x1ce87d0, 0x1d20ed0, 0x1d11f70, 0x1cd4cf0, 0x1ccecf0, 0x1cf6d30, 0x1d20a90, 0x1d28d90, 0x1cfd3b0, 0x1d28c90, 0x1d03f50, 0x1cff790, 0x1d0ad70, 0x1c869f0, 0x1d322d0, 0x1d20650, 0x1ce8cf0, 0x1c9adb0, 0x1cdd990, 0x1ccd370, 0x1d1edd0, 0x1c8fe10, 0x1cb73d0, 0x1cdee10, 0x1ce07b0, 0x1c9a890, 0x1cb30b0, 0x1cf1a50, 0x1ce4f70, 0x1c8b6b0, 0x1d26e60, 0x1d21210, 0x1d342d0, 0x1cfba10, 0x1ceeb70, 0x1c805d0, 0x1c89e30, 0x1cff270, 0x1c8eeb0, 0x1cf81b0, 0x1d22150, 0x1cc03b0, 0x1d12ed0, 0x1d20dd0, 0x1cce7d0, 0x1d058f0, 0x1d31e10, 0x1c82c30, 0x1c8cf10, 0x1cd8790, 0x1c7e910, 0x1d20990, 0x1cdf330, 0x1d28b90, 0x1cacf50, 0x1d30d90, 0x1cc95b0, 0x1cc3e50, 0x1ce5ed0, 0x1c917b0, 0x1cbd090, 0x1cd0f70, 0x1d362d0, 0x1d0eaf0, 0x1cf4c70, 0x1caaf90, 0x1cb8d70, 0x1cadeb0, 0x1cf33f0, 0x1d0f010, 0x1cd6690, 0x1c822b0, 0x1c95030, 0x1d22670, 0x1d006f0, 0x1d21110, 0x1d10af0, 0x1cef090, 0x1d26430, 0x1ce0cd0, 0x1ceb0d0, 0x1d28ed0, 0x1c9b2d0, 0x1cc57f0, 0x1cf9110, 0x1d20a50, 0x1c97030, 0x1d20890, 0x1d01130, 0x1d19150, 0x1cd3d90, 0x1c98ef0, 0x1d20450, 0x1d28c50, 0x1cc22b0, 0x1cfb4f0, 0x1cd91d0, 0x1cdf850, 0x1cb11f0, 0x1d28210, 0x1d30e50, 0x1ca6bb0, 0x1d08c30, 0x1d12490, 0x1cd5210, 0x1cc4db0, 0x1d34250, 0x1c9f230, 0x1cdbad0, 0x1cf7250, 0x1cfe310, 0x1ce30b0, 0x1d21010, 0x1cc7190, 0x1d0b290, 0x1cb5510, 0x1d07290, 0x1c989d0, 0x1d20bd0, 0x1cc52d0, 0x1d28dd0, 0x1c856f0, 0x1d30fd0, 0x1d20790, 0x1c8c070, 0x1cd3350, 0x1cfce90, 0x1cc4890, 0x1d343d0, 0x1d03a30, 0x1d25ab0, 0x1d20350, 0x1cdd470, 0x1c8d3d0, 0x1ccce50, 0x1cc76f0, 0x1ce4010, 0x1c82770, 0x1c88b30, 0x1ceabb0, 0x1d34410, 0x1ccf410, 0x1cb6eb0, 0x1c9a370, 0x1cb2b90, 0x1cf1530, 0x1d20f10, 0x1cb7e10, 0x1cd1490, 0x1d19f30, 0x1cd47d0, 0x1d27890, 0x1c894b0, 0x1d20ad0, 0x1cf7c90, 0x1d28cd0, 0x1c9de10, 0x1cbfe90, 0x1cfe830, 0x1cb2150, 0x1cecbb0, 0x1d053d0, 0x1d03510, 0x1d20690, 0x1cd2e30, 0x1ca9530, 0x1cd8270, 0x1d23970, 0x1c97550, 0x1cc9090, 0x1cc3930, 0x1d20250, 0x1c91290, 0x1ce3af0, 0x1cbcb70, 0x1d0e5d0, 0x1cf4750, 0x1c8f8f0, 0x1cb8850, 0x1cad990, 0x1cb35d0, 0x1d21250, 0x1d09e70, 0x1cefff0, 0x1cd6170, 0x1c94b10, 0x1ced650, 0x1d20e10, 0x1cf9630, 0x1cd2910, 0x1ca9010, 0x1c93670, 0x1d001d0, 0x1d06d70, 0x1c881b0, 0x1d209d0, 0x1d33a90, 0x1d28bd0, 0x1cd9c10, 0x1d30dd0, 0x1c8f3d0, 0x1ce7350, 0x1c92c30, 0x1cbe510, 0x1d20590, 0x1ccf930, 0x1c8a810, 0x1cf60f0, 0x1cba1f0, 0x1c96b10, 0x1caf330, 0x1c9ed10, 0x1c9f750, 0x1d1e8d0, 0x1d34290, 0x1cc1d90, 0x1cfafd0, 0x1c8ca30, 0x1d01b70, 0x1d20d10, 0x1caf850, 0x1d28f10, 0x1ce7870, 0x1cb4ff0, 0x1d208d0, 0x1cbbb90, 0x1c984b0, 0x1d30cd0, 0x1c818d0, 0x1cf2ed0, 0x1d247b0, 0x1d20490, 0x1cf3910, 0x1d09430, 0x1c99930, 0x1c87830, 0x1d33110, 0x1cbf980, 0x1ca8030, 0x1d13910, 0x1cd19b0, 0x1cdcf50, 0x1d0d150, 0x1d21050, 0x1cea690, 0x1d0c710, 0x1cb5a30, 0x1cb6990, 0x1d24c70, 0x1cf7770, 0x1d20c10, 0x1d28e10, 0x1c99e50, 0x1cb2670, 0x1d27370, 0x1c83a70, 0x1c81410, 0x1d207d0, 0x1cefad0, 0x1d1e250, 0x1d20950, 0x1d20390, 0x1cb3b10, 0x1ca8590, 0x1cc8650, 0x1d04eb0, 0x1d217d0, 0x1d1f2f0, 0x1cf9b50, 0x1cf2490, 0x1cde8f0, 0x1cc8b70, 0x1d34450, 0x1ce5490, 0x1d1fd30, 0x1c8bb90, 0x1c90d70, 0x1cbc650, 0x1c8e0b0, 0x1cb8330, 0x1cad470, 0x1cf5bd0, 0x1d30d50, 0x1d20f50, 0x1cf29b0, 0x1c8b1d0, 0x1c7fc10, 0x1c86eb0, 0x1ccb4b0, 0x1d32790, 0x1cb1c30, 0x1d20b10, 0x1d28d10, 0x1cf1f70, 0x1d0e0b0, 0x1d206d0, 0x1d06850, 0x1cffcb0, 0x1c91cd0, 0x1cd96f0, 0x1c87cf0, 0x1ce0290, 0x1cca510, 0x1cc5d10, 0x1ce6e30, 0x1c92710, 0x1cbdff0, 0x1d0fa50, 0x1c80a90, 0x1c8a2f0, 0x1cb9cd0, 0x1c7ddd0, 0x1c965f0, 0x1caee10, 0x1ccaf90, 0x1c9e7f0, 0x1cdfd70, 0x1d21290, 0x1d27d50, 0x1c81d98, 0x1cab4f0, 0x1c830f0, 0x1cd0a50, 0x1cf3dd0, 0x1c7edd0, 0x1ca9a50, 0x1c84d70, 0x1cfaab0, 0x1cfed50, 0x1d05e10, 0x1d01650, 0x1c8e5d0, 0x1d36790, 0x1d081f0, 0x1d20a10, 0x1d11a50, 0x1d28c10, 0x1d30e10, 0x1cdb090, 0x1ccaa70, 0x1d23e30, 0x1ce1c30, 0x1d205d0, 0x1d0a850, 0x1c940b0, 0x1cb4ad0, 0x1c7ccd0, 0x1c86530, 0x1cd1ed0, 0x1ce59b0, 0x1cbb670, 0x1c97f90, 0x1cb07b0, 0x1d0f530, 0x1d25f70, 0x1cd23f0, 0x1d21190, 0x1cfc450, 0x1ccdeb0, 0x1d02ff0, 0x1ca7b10, 0x1d133f0, 0x1c75470, 0x1d20d50, 0x1cee6b0, 0x1c89970, 0x1cdca30, 0x1ccfeb0, 0x1ccfe50, 0x1ccff10, 0x1cc3570, 0x1d17630, 0x1ccf210, 0x1cc3650, 0x1cc3490, 0x1d17550, 0x1d17230, 0x1d179b0, 0x1cc2fd0, 0x1cce6b0, 0x1cc3190, 0x1d17390, 0x1d178d0, 0x1d17470, 0x1d177f0, 0x1cc30b0, 0x1d17710, 0x1cee650, 0x1cf0510, 0x1cf0570, 0x1d19630, 0x1d19610, 0x1c74190, 0x1c742d0, 0x1c743b0, 0x15e4810, 0x1d1a430, 0x15e4850, 0x1d19670, 0x1d3ae90, 0x1d1a470, 0x15e4890, 0x1c74310, 0x1d36250, 0x1d1a4b0, 0x1d3aed0, 0x15e47d0, 0x1c74350, 0x1d14b90, 0x1d14e90, 0x1d14d10, 0x1d19950, 0x1d19990, 0x1d160c8, 0x1d161d0, 0x1d16408, 0x1d16430, 0x1d16690, 0x1d16520, 0x1d16548, 0x1d16db0, 0x1d16638, 0x1d16660, 0x1d16b90, 0x1d16bd0, 0x1d160f0, 0x1d16768, 0x1d18bf0, 0x1d187d8, 0x1d16908, 0x1d15ff0, 0x1d15bb0, 0x1d169d8, 0x1d16a10, 0x1d16a88, 0x1d16c70, 0x1d16ab0, 0x1d18b30, 0x1d16740, 0x1d16850, 0x1d16890, 0x1d16c38, 0x1d16cd8, 0x1d18770, 0x1d16d78, 0x1d16e18, 0x1d16e50, 0x1d16d10, 0x1d16ef0, 0x1d16350, 0x1d16590, 0x1d16eb8, 0x1d16fa0, 0x1d16fc8, 0x1d16470, 0x1d16030, 0x1d167b0, 0x1d199d0, 0x1d16af0, 0x1d16270, 0x1d18150, 0x1d16390, 0x1d16970, 0x1d16190, 0x1d15f50, 0x1d18c50, 0x1d15f90, 0x1d16930, 0x1d162b0, 0x1d15f10, 0x1d29d90, 0x1d29dd0, 0x1d29d10, 0x1d345f0, 0x1d298f0, 0x1d1a4f0, 0x1cc0df0, 0x1d142f0, 0x1c74490, 0x1d1a3f0, 0x1d17c90, 0x1d15a90, 0x1d18730, 0x1d1a530, 0x1d29d50, 0x1c744d0, 0x1c7cc30, 0x1cbc5d0, 0x1d17cd0, 0x1c7d190, 0x1d29970, 0x1d1c350, 0x1c74510, 0x1d17dd0, 0x1d17d10, 0x1d17d50, 0x1d1c7b0, 0x1d30230, 0x1c74450, 0x1d15a10, 0x1d15a50, 0x1d18f30, 0x1d17c50, 0x1d17d90, 0x1d1cb30, 0x1d2a190, 0x1d2a2d0, 0x1d2a0f0, 0x1d2a230, 0x1d2a370, 0x1d2a050, 0x1d2a010, 0x1d29f30, 0x1c746b0, 0x15f80b0, 0x1c746f0, 0x1d2a410, 0x1d3b0b0, 0x1d15070, 0x15e3c90, 0x1d1e870, 0x1d2fef0, 0x1d2a470, 0x1d2e1c0, 0x1d2c3e8, 0x1d2b180, 0x1d2eac8, 0x1d2ad40, 0x1d2af40, 0x1d2bd80, 0x1d2b520, 0x1d2b720, 0x1d2fa60, 0x1d2bb78, 0x1d2fcc0, 0x1d2bf80, 0x1d2c078, 0x1d2e0a8, 0x1d2f050, 0x1d2c140, 0x1d2fc10, 0x1d2d5a8, 0x1d2e170, 0x1d2c238, 0x1d2e2a8, 0x1d2f608, 0x1d2e488, 0x1d2c4e0, 0x1d1e830, 0x1d2c5a8, 0x1d2e688, 0x1d2c698, 0x1d2de68, 0x1d2e858, 0x1d2a998, 0x1d2c9f8, 0x1d2ec78, 0x1d2bc70, 0x1d2ac48, 0x1d2ed88, 0x1d2cdb8, 0x1d2ae28, 0x1d2cf48, 0x1d2bd38, 0x1d2ef88, 0x1d2b028, 0x1d2d148, 0x1d2f158, 0x1d2b0f0, 0x1d2e750, 0x1d2b278, 0x1d2b340, 0x1d2c870, 0x1d2d3c8, 0x1d2f438, 0x1d2dd50, 0x1d2b458, 0x1d2d210, 0x1d2f500, 0x1d2aef0, 0x1d2ebb0, 0x1d2b608, 0x1d2be68, 0x1d2dab0, 0x1d2d7a8, 0x1d2f7f8, 0x1d2b818, 0x1d2d870, 0x1d2b8e0, 0x1d2f988, 0x1d2b9d8, 0x1d2a8b0, 0x1d2fb48, 0x1d2d9e8, 0x1d2dc88, 0x1d2bf30, 0x1d2cbb0, 0x1d2fe00, 0x1d2e370, 0x1d2fec8, 0x1d2b6d0, 0x1d2d490, 0x1d2aa98, 0x1d2c360, 0x1d2c5d8, 0x1d2b918, 0x1d2c778, 0x1d2e798, 0x1d2c178, 0x1d2c938, 0x1d2e9a0, 0x1d2cab8, 0x1d2ccb8, 0x1d2f098, 0x1d2f280, 0x1d2b398, 0x1d2bb00, 0x1d2fd30, 0x1d2e560, 0x1d2df80, 0x1d2ea30, 0x1d2ab78, 0x1d2ecb8, 0x1d2ce78, 0x1d2d020, 0x1d2dd98, 0x1d2d2a0, 0x1d2f310, 0x1d2d4d8, 0x1d2f538, 0x1d2ee60, 0x1d2e3b8, 0x1d2d680, 0x1d2f6f8, 0x1d2f8b8, 0x1d2d8c0, 0x1d2db60, 0x1d30390, 0x1d302b0, 0x1d30550, 0x1d307b0, 0x1d30150, 0x1d30970, 0x1d30890, 0x1d30a50, 0x1d30470, 0x1d35750, 0x1d35690, 0x1cecb10, 0x1d18950, 0x1d188b0, 0x1d18cb0, 0x1d29f70, 0x1d1a650, 0x1ceca70, 0x1d18a90, 0x1ced0b0, 0x1d35830, 0x1d351d0, 0x1d1a7b0, 0x1d17050, 0x1d189f0, 0x1d1a5b0, 0x1cebeb0, 0x1d198b0, 0x1d354b0, 0x1d35330, 0x1d35790, 0x1d18810, 0x1cebe10, 0x1cebf50, 0x1d35af0, 0x1d18d90, 0x1d35a10, 0x1d18df0, 0x1d35cb0, 0x1d35bd0, 0x1d19d70, 0x1d36030, 0x1d347b0, 0x1d36110, 0x1d1cd70, 0x1d35f30, 0x1d1e710, 0x1d358d0, 0x1d1cc70, 0x1d34830, 0x1d355b0, 0x1d36170, 0x1d34770, 0x1d348f0, 0x1d1a850, 0x1d1e7f0, 0x1d35f70, 0x1d19db0, 0x1d1a750, 0x1d18ff0, 0x1d1ccb0, 0x1d18ef0, 0x1d353d0, 0x1d34930, 0x1d35930, 0x1d19cf0, 0x1d35fb0, 0x1d34730, 0x1d1ccf0, 0x1d360d0, 0x1d34870, 0x1d19790, 0x1d197d0, 0x1d35430, 0x1d19d30, 0x1d35ff0, 0x1d1cd30, 0x1d35ef0, 0x1d3aff0, 0x1d1cc30, 0x1d347f0, 0x1d34130, 0x1d18fb0, 0x1d18f70, 0x1d3a018, 0x1d38ab8, 0x1d38058, 0x1d378b0, 0x1d38098, 0x1d3a0b8, 0x1d380c0, 0x1d35e10, 0x1d39f10, 0x1d3a0f8, 0x1d37ad8, 0x1d38138, 0x1d38188, 0x1d39470, 0x1d3a1f8, 0x1d38630, 0x1d38228, 0x1d3a470, 0x1d38278, 0x1d3a5c0, 0x1d387b0, 0x1d38318, 0x1d3a340, 0x1d39b38, 0x1d38398, 0x1d37d10, 0x1d378d0, 0x1d38480, 0x1d3a4c8, 0x1d38580, 0x1d15b90, 0x1d37b00, 0x1599100, 0x1d3a6c0, 0x1d3a120, 0x1d395b0, 0x1d3a158, 0x1d39c08, 0x1d38b58, 0x1d39398, 0x1d3a8b8, 0x1d388d8, 0x1d387f0, 0x1d377f0, 0x1d39700, 0x1d39c58, 0x1d3a370, 0x1d38a58, 0x1d38a80, 0x1d37b60, 0x1d39c30, 0x1d38bd8, 0x1d38ca0, 0x1d38cd8, 0x1d37c50, 0x1d38d80, 0x1d39240, 0x1d37810, 0x1d38df8, 0x1d39278, 0x1d38ee8, 0x1d3a810, 0x1d37910, 0x1599290, 0x1d37930, 0x1d38f98, 0x1d38fc0, 0x1d38ff8, 0x1d38710, 0x1599130, 0x1c741d0, 0x1d390a0, 0x15990d8, 0x1d37c70, 0x1d39118, 0x1d38e90, 0x1d37830, 0x1d391c0, 0x1d391e8, 0x1d39218, 0x1d38c78, 0x1d3a318, 0x1d39878, 0x15992f8, 0x1d37dd8, 0x1599320, 0x1d39328, 0x1d3ac78, 0x1d39c80, 0x1d394b8, 0x1d37950, 0x1d37850, 0x1d39588, 0x1d39628, 0x1d3a570, 0x1d3a3c0, 0x1d396d8, 0x1d37970, 0x1d38db0, 0x1d39738, 0x1d38970, 0x1599390, 0x1d37b98, 0x1d38530, 0x1d39970, 0x1d39808, 0x1d39ec8, 0x1d3a278, 0x1d37a90, 0x1d37870, 0x1d39948, 0x1d39998, 0x1d39448, 0x1d379b8, 0x1d399c0, 0x1d38430, 0x1d399f8, 0x1599150, 0x1d3aa90, 0x1d37a40, 0x1d3ab38, 0x1d39ac8, 0x1d37b38, 0x1d379e0, 0x1d37bc0, 0x1d3a9f8, 0x1d37bf8, 0x1d37c20, 0x1d3a950, 0x1d378f0, 0x1d37a18, 0x1d37890, 0x1d39cb8, 0x1d37f78, 0x1d389a0, 0x1d35df0, 0x1d39ef0, 0x1d38890, 0x15992b0, 0x1d38670, 0x1d39d88, 0x1d37a70, 0x1d39df8, 0x1d3a670, 0x1d37e88, 0x1d37ed8, 0x1d39f58, 0x1d38350, 0x1d37fb8, 0x1d3abd0, 0x1d3b150, 0x1d3b4d0, 0x1d3b1b0, 0x1d3b3f0, 0x1d3b230, 0x1d3b550, 0x1d3b2b0, 0x1d3b770, 0x1d3b890, 0x1d3af10, 0x1d1c710, 0x1d1c650, 0x1d1c6b0, 0x1d3b690, 0x1d3b6f0, 0x1d3b0f0, 0x159b630, 0x159add0, 0x15ab070, 0x15ab050, 0x1d14990, 0x159ca50, 0x1d149b0, 0x15a9870, 0x159ae50, 0x15fbc70, 0x15df670, 0x159ca70, 0x15a9e90, 0x15a8d90, 0x15ded50, 0x15fc2b0, 0x159adf0, 0x1d149d0, 0x159b478, 0x15fa730, 0x1c7d1d0, 0x15a9890, 0x15fb630, 0x15fbc90, 0x159b5d0, 0x15facd0, 0x159ae70, 0x15a9fe8 ]



DEBUG = True

subvtable_candidates = list()
basevtable_candidates = list()
for vtable in vtables:

    ott = Qword(vtable-16)
    if ott != 0:
        subvtable_candidates.append(vtable)
        if DEBUG:
            print "0x%x - SUBVTABLE" % vtable
    else:
        basevtable_candidates.append(vtable)
        if DEBUG:
            print "0x%x - BASEVTABLE" % vtable


print
print "Possible base-vtables:"
for vtable in basevtable_candidates:
    print "0x%x" % vtable
print

print "Possible sub-vtables:"
for vtable in subvtable_candidates:
    print "0x%x" % vtable
print