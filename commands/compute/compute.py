from commands.base_command import BaseCommand
from dao.base_dao import DBResultError
from dao.compute_dao import compute_dao


class GetComputeJobInfo(BaseCommand):
    def __init__(self, compute_job_info_id: str):
        super(GetComputeJobInfo, self).__init__()
        self.compute_job_info_id = compute_job_info_id

    def execute(self):
        try:
            job_info = compute_dao.get_compute_info(self.compute_job_info_id)
            result = {'id': job_info['_id'], 'parameters': job_info['parameters']}
            self.successful = True
            return result
        except DBResultError:
            self.successful = False
            self.messages = [str(e)]


class CreateComputeJobInfo(BaseCommand):
    def __init__(self, public_address: str, entity_list_id: list, parameters: dict):
        super(CreateComputeJobInfo, self).__init__()
        self.parameters = parameters
        self.public_address = public_address
        self.entity_list_id = entity_list_id

    def execute(self):
        details_id = compute_dao.create_compute_input(self.public_address, self.entity_list_id, self.parameters)
        self.successful = True
        return details_id
