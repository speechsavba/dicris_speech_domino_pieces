from domino.base_piece import BasePiece
#from pieces.RandomNumPiece.models import InputModel1, OutputModel1
#from pieces.RandomNumPiece.piece import RandomNumPiece
from domino.testing import piece_dry_run
input_data1 = dict(max_num=100,min_num=90)
output_data1 = piece_dry_run("RandomNumPiece",input_data1,)
print(output_data1)
print('*'*10)
input_data2 = dict(max_num=-10,min_num=-20)
output_data2 = piece_dry_run("RandomNumPiece",input_data2)
print(output_data2)
print('*'*10)
input_data3 = dict(a_num=output_data1['number'],b_num=output_data2['number'])
output_data3 = piece_dry_run("CalcSumPiece",input_data3)
print(output_data3)
print('*'*10)