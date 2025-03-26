import json
class JSONFormatter:
    @staticmethod
    def generate_json(matrix):
        result = {}
        for i, row in enumerate(matrix, start=1):
            row_key = f"Row{i}"
            row_data = []
            for j, (r, g, b) in enumerate(row, start=1):
                tube_key = f"Tube{j}"
                row_data.append({
                    tube_key: {
                        "R": round(r, 2),
                        "G": round(g, 2),
                        "B": round(b, 2)
                    }
                })
            result[row_key] = row_data
        return json.dumps(result, indent=2)