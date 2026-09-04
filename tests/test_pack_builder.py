import importlib.util, json, tempfile, unittest
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]; SCRIPT=ROOT/"scripts"/"render_banner_pack.py"
def load_module():
    spec=importlib.util.spec_from_file_location("render_banner_pack",SCRIPT); m=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(m); return m

class PackBuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=load_module(); renderer_spec=importlib.util.spec_from_file_location("renderer",ROOT/"scripts"/"render_banner.py"); cls.r=importlib.util.module_from_spec(renderer_spec); assert renderer_spec.loader; renderer_spec.loader.exec_module(cls.r); cls.font=cls.r.resolve_font_path(None)
    def base_spec(self,job,w,h,family,out):
        return {"job_id":job,"width":w,"height":h,"layout_family":family,"background":{"color":"#FFFFFF"},"hero":None,"logo":{"brand_name":"BRAND"},"copy":{"headline":"Кухни на заказ","support":None,"offer":None,"cta":"Рассчитать"},"brand":{"font_regular":self.font,"font_bold":self.font,"text_color":"#111111","cta_fill":"#111111","cta_text":"#FFFFFF"},"output":{"path":str(out),"format":"png"}}
    def test_complete_matrix_returns_pack_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); specs=root/"specs"; specs.mkdir(); outputs=root/"out"; rows=[]
            for job,w,h,fam in [("C01-S300x250-V01-Lru",300,250,"rectangle"),("C01-S320x50-V01-Lru",320,50,"micro_horizontal")]:
                out=outputs/job/f"{job}.png"; row={"job_id":job,"width":w,"height":h,"layout_family":fam,"output_path":str(out),"output_format":"png"}; rows.append(row); (specs/f"{job}.json").write_text(json.dumps(self.base_spec(job,w,h,fam,out),ensure_ascii=False),encoding="utf-8")
            matrix={"run_id":"demo","expected_output_files":2,"banner_matrix":rows}
            def validator(path,mode,pack):
                with Image.open(path) as im: size=im.size
                return {"status":"PASS","errors":[],"dimension":f"{size[0]}x{size[1]}"}
            result=self.m.render_pack(matrix,specs,contact_sheet=root/"sheet.png",manifest_path=root/"manifest.json",technical_validator=validator)
            self.assertEqual(result["status"],"PASS"); self.assertEqual(result["passed_output_files"],2); self.assertTrue((root/"sheet.png").is_file()); self.assertTrue((root/"manifest.json").is_file())
            manifest=json.loads((root/"manifest.json").read_text(encoding="utf-8")); self.assertEqual(len(manifest["files"]),2); self.assertTrue(all(item["status"]=="PASS" for item in manifest["files"]))
    def test_real_google_validator_integrates_with_pack_runner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); specs=root/"specs"; specs.mkdir(); job="C01-S300x250-V01-Lru"; out=root/"out"/f"{job}.png"
            row={"job_id":job,"concept_id":"C01","variant_id":"V01","width":300,"height":250,"layout_family":"rectangle","output_path":str(out),"output_format":"png"}
            (specs/f"{job}.json").write_text(json.dumps(self.base_spec(job,300,250,"rectangle",out),ensure_ascii=False),encoding="utf-8")
            result=self.m.render_pack({"run_id":"integration","expected_output_files":1,"banner_matrix":[row]},specs,mode="demand_gen_uploaded_display",pack="core")
            self.assertEqual(result["status"],"PASS"); self.assertEqual(result["jobs"][0]["validation"]["status"],"PASS")
    def test_missing_spec_blocks_full_pack(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); specs=root/"specs"; specs.mkdir(); matrix={"run_id":"demo","expected_output_files":1,"banner_matrix":[{"job_id":"missing","width":300,"height":250,"layout_family":"rectangle","output_path":str(root/"missing.png"),"output_format":"png"}]}
            result=self.m.render_pack(matrix,specs,technical_validator=lambda *args:{"status":"PASS","errors":[]})
            self.assertEqual(result["status"],"FAIL"); self.assertEqual(result["failed_output_files"],1); self.assertEqual(result["failures"][0]["job_id"],"missing")
    def test_failed_pack_does_not_emit_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); specs=root/"specs"; specs.mkdir(); manifest=root/"manifest.json"; matrix={"run_id":"demo","expected_output_files":1,"banner_matrix":[{"job_id":"missing","width":300,"height":250,"layout_family":"rectangle","output_path":str(root/"missing.png"),"output_format":"png"}]}
            result=self.m.render_pack(matrix,specs,manifest_path=manifest,technical_validator=lambda *args:{"status":"PASS","errors":[]})
            self.assertEqual(result["status"],"FAIL"); self.assertFalse(manifest.exists())
    def test_spec_matrix_mismatch_fails_job(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); specs=root/"specs"; specs.mkdir(); job="j"; row={"job_id":job,"width":300,"height":250,"layout_family":"rectangle","output_path":str(root/"j.png"),"output_format":"png"}; bad=self.base_spec(job,336,280,"rectangle",root/"x.png"); (specs/"j.json").write_text(json.dumps(bad),encoding="utf-8"); result=self.m.render_pack({"expected_output_files":1,"banner_matrix":[row]},specs,technical_validator=lambda *args:{"status":"PASS","errors":[]}); self.assertEqual(result["failures"][0]["code"],"FAIL_SPEC_MATRIX_MISMATCH")
if __name__=="__main__": unittest.main()
