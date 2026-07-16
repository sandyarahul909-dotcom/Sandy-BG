import os
import cv2
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView

class SandyBGApp(App):
    def build(self):
        self.title = "Sandy BG"
        self.selected_video = None
        self.selected_image = None
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        self.label = Label(text="Sandy BG - Ultra Smooth DNN Changer", font_size=18, size_hint_y=0.1)
        layout.add_widget(self.label)
        self.file_chooser = FileChooserIconView(size_hint_y=0.5)
        layout.add_widget(self.file_chooser)
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=10)
        self.vid_btn = Button(text="1. Select Video", background_color=(0.2, 0.6, 1, 1))
        self.vid_btn.bind(on_press=self.select_video)
        btn_layout.add_widget(self.vid_btn)
        self.img_btn = Button(text="2. Select BG Photo", background_color=(0.2, 0.6, 1, 1))
        self.img_btn.bind(on_press=self.select_image)
        btn_layout.add_widget(self.img_btn)
        layout.add_widget(btn_layout)
        self.process_btn = Button(text="3. Replace Background (Stable)", size_hint_y=0.2, background_color=(0, 0.7, 0.3, 1))
        self.process_btn.bind(on_press=self.remove_background)
        layout.add_widget(self.process_btn)
        return layout

    def select_video(self, instance):
        if self.file_chooser.selection:
            self.selected_video = self.file_chooser.selection[0]
            self.label.text = f"Selected Video: {os.path.basename(self.selected_video)}"

    def select_image(self, instance):
        if self.file_chooser.selection:
            self.selected_image = self.file_chooser.selection[0]
            self.label.text = f"Selected BG Photo: {os.path.basename(self.selected_image)}"

    def remove_background(self, instance):
        if not self.selected_video or not self.selected_image:
            self.label.text = "Error: Select both Video and BG Photo!"
            return
        self.label.text = "Processing Clear Video via DNN... Please wait..."
        output_path = os.path.join(os.path.dirname(self.selected_video), "SandyBG_DNN_Output.mp4")
        model_path = "selfie_segmentation.onnx"
        if not os.path.exists(model_path):
            self.label.text = "Error: AI Model file missing!"
            return
        net = cv2.dnn.readNetFromONNX(model_path)
        cap = cv2.VideoCapture(self.selected_video)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        bg_photo = cv2.imread(self.selected_image)
        bg_photo = cv2.resize(bg_photo, (width, height))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        prev_mask = None
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            blob = cv2.dnn.blobFromImage(frame, 1.0/255.0, (256, 256), (0,0,0), swapRB=True, crop=False)
            net.setInput(blob)
            output = net.forward()
            mask = output[0, 0, :, :]
            mask = cv2.resize(mask, (width, height))
            if prev_mask is not None:
                mask = cv2.addWeighted(mask, 0.7, prev_mask, 0.3, 0)
            prev_mask = mask.copy()
            mask = cv2.GaussianBlur(mask, (11, 11), 0)
            mask_3d = np.stack((mask,) * 3, axis=-1)
            frame = frame.astype(float)
            bg_photo_float = bg_photo.astype(float)
            output_frame = (mask_3d * frame + (1.0 - mask_3d) * bg_photo_float).astype(np.uint8)
            out.write(output_frame)
        cap.release()
        out.release()
        self.label.text = f"Saved: {os.path.basename(output_path)}"

if __name__ == '__main__':
    SandyBGApp().run()