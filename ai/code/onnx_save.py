import numpy as np
import torch
import torchvision
import onnx
import onnxruntime


def save_to_onnx(model, input_img, save_path):
    torch.onnx.export(model, input_img, save_path, export_params=True, opset_version=11)


def save_to_pth(model, save_path):
    torch.jit.save(torch.jit.script(model), save_path)


def load_onnx(save_path):
    model = onnx.load(save_path)
    return model

def onnx_run():
    runtime_session = onnxruntime.InferenceSession("resnet18.onnx")

    dummy_input = np.random.randn(1, 3, 224, 224).astype(np.float32)

    outputs = runtime_session.run(None, {"input.1": dummy_input})
    print(outputs)


def main():
    model = torchvision.models.resnet18(weights=torchvision.models.ResNet18_Weights.IMAGENET1K_V1)

    input_image = torch.randn(1, 3, 224, 224)

    save_to_onnx(model, input_image, 'resnet18.onnx')

    save_to_pth(model, 'resnet18.pth')

    onnx_model = load_onnx('resnet18.onnx')
    onnx.checker.check_model(onnx_model)

    output = onnx_model.producer_name
    print(output)

    # onnx_run()




if __name__ == "__main__":
    main()
