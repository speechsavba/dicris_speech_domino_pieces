from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from time import sleep


class CalcSumPiece(BasePiece):

	def piece_function(self, input_data: InputModel):

		self.logger.info(f"Make sum for {input_data.a_num} {input_data.b_num}")
		ab_sum=input_data.a_num+input_data.b_num

		message = f"The sum of {input_data.a_num} and {input_data.b_num} is {ab_sum}"
		self.logger.info(message)
		# Return output
		return OutputModel(
			message=message,
		)
