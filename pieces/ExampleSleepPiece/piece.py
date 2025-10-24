from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from time import sleep


class ExampleSleepPiece(BasePiece):

    def piece_function(self, input_data: InputModel):

        self.logger.info(f"Sleeping for {input_data.sleep_time} seconds")
        sleep(input_data.sleep_time)
        message = f"Sleep piece executed successfully for {input_data.sleep_time} seconds"
        self.logger.info(message)
        self.logger.info('Blablabla')
        output_file_path = f"{self.results_path}/sleeping.txt"
        fout = open(output_file_path, "w")
        fout.write(f"Sleeping for {input_data.sleep_time} seconds")
        fout.close()

        # Return output
        return OutputModel(
            message=message,
        )
