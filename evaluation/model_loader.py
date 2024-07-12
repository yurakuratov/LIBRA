import torch
import transformers

from transformers import LlamaTokenizer, AutoModelForCausalLM, AutoTokenizer, AutoConfig


class ModelLoader():
    def __init__(self, model_path, model_torch_dtype, tokenizer_path=None, device="cpu"):
        self.model_path = model_path
        self.device = device
        self.model_torch_dtype = self.get_dtype(model_torch_dtype)
        if tokenizer_path:
            self.tokenizer_path = tokenizer_path
        else:
            self.tokenizer_path = model_path
    
    def get_dtype(self, dtype):
        dct_dtypes = {
                    "float16": torch.float16,
                    "bfloat16": torch.bfloat16,
                    "float32": torch.float
                     }
        if dtype in dct_dtypes:
            return dct_dtypes[dtype]
        else:
            return torch.float
        

    def model_load(self):
        config = transformers.AutoConfig.from_pretrained(
        self.model_path,
        )
        if "LlamaForCausalLM" in config.architectures:
            model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                attn_implementation='flash_attention_2',
                trust_remote_code=True,
                torch_dtype=self.model_torch_dtype,
            ).eval().to(self.device)
        else:
            model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                torch_dtype=self.model_torch_dtype,
            ).eval().to(self.device)
        tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path, trust_remote_code=True)
        return model, tokenizer
