import importlib.util, json, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SCRIPT=ROOT/"scripts"/"materialize_banner_jobs.py"
def load_module():
    spec=importlib.util.spec_from_file_location("materialize_banner_jobs",SCRIPT); m=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(m); return m
class MaterializeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.m=load_module()
    def matrix(self):
        return {"run_id":"demo","expected_output_files":2,"banner_matrix":[
            {"job_id":"C01-S300x250-V01-Lru","concept_id":"C01","variant_id":"V01","language":"ru","width":300,"height":250,"layout_family":"rectangle","headline":"Кухни на заказ","cta":"Рассчитать","output_format":"png","output_path":"outputs/demo/a.png"},
            {"job_id":"C01-S320x50-V01-Lru","concept_id":"C01","variant_id":"V01","language":"ru","width":320,"height":50,"layout_family":"micro_horizontal","output_format":"png","output_path":"outputs/demo/b.png"}]}
    def test_creates_one_spec_and_brief_per_row_without_inventing_missing_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"run"; result=self.m.materialize(self.matrix(),out); self.assertEqual(len(result["jobs"]),2)
            first=json.loads((out/"render-specs"/"C01-S300x250-V01-Lru.json").read_text(encoding="utf-8")); second=json.loads((out/"render-specs"/"C01-S320x50-V01-Lru.json").read_text(encoding="utf-8"))
            self.assertEqual(first["copy"]["headline"],"Кухни на заказ"); self.assertEqual(first["copy"]["cta"],"Рассчитать"); self.assertIsNone(second["copy"]["headline"]); self.assertEqual(second["brand"],{}); self.assertTrue((out/"task-briefs"/"C01-S320x50-V01-Lru.md").is_file()); self.assertTrue((out/"dispatch-index.json").is_file())
    def test_refuses_to_overwrite_existing_worker_files_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"run"; self.m.materialize(self.matrix(),out)
            with self.assertRaises(self.m.MaterializeError): self.m.materialize(self.matrix(),out)
    def test_force_recreates_shells_when_controller_explicitly_requests_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"run"; self.m.materialize(self.matrix(),out); path=out/"render-specs"/"C01-S300x250-V01-Lru.json"; path.write_text("changed",encoding="utf-8"); self.m.materialize(self.matrix(),out,force=True); self.assertIn('"job_id": "C01-S300x250-V01-Lru"',path.read_text(encoding="utf-8"))
if __name__=="__main__": unittest.main()
