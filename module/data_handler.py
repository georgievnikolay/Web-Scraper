import json

class DataHandler:
    @staticmethod
    def data_frame_to_json(df, file_name):
        df.to_json(file_name, force_ascii=False, orient='records', indent=4)

    @staticmethod
    def obj_to_json(obj, file_name):
        with open(file_name, 'w') as f:
            json.dump(obj, f, indent=4, ensure_ascii=False)

    @staticmethod
    def json_to_obj(file_name):
        with open(file_name, 'r') as f:
            return json.load(f)
