import json

class DataHandler:
    """
    Helper class that handles reading and writing json files.
    """

    @staticmethod
    def data_frame_to_json(df, file_name):
        df.to_json(file_name, force_ascii=False, orient='records', indent=4)

    @staticmethod
    def obj_to_json(obj, file_name):
        with open(file_name, 'w', encoding='utf-8-sig') as f:
            json.dump(obj, f, indent=4, ensure_ascii=False)

    @staticmethod
    def json_to_obj(file_name):
        with open(file_name, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
