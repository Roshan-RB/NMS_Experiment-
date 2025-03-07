# OCR Text Detection with Non-Maximum Suppression (NMS)

## 🧐 What is this project about?
This project is all about **detecting words from an image** using **EasyOCR**, but with a twist! Instead of just reading text, we go a step further and apply **Modified Non-Maximum Suppression (NMS)** to remove duplicate detections caused by overlapping image regions.

## 🏆 Goal of the Project
- **Generate a random image with text** for testing OCR.
- **Accurately detect words** from the image using EasyOCR.
- **Divide the image into 4 overlapping regions** to improve OCR detection.
- **Remove duplicate detections** using a smart filtering method (NMS).
- **Get an accurate count** of detected words.

---

## 🛠️ How does it work?
### 🔹 Step 1: Generating a Random Image with Fruit Names
Before running OCR, we needed an **image with randomly placed fruit names**. To achieve this, we wrote a script that:
- Creates a **blank image**.
- Randomly places the words **'mango', 'banana', 'strawberry', and 'orange'** multiple times.
- Ensures words are placed at **different positions** to simulate real-world randomness.
- Saves the generated image for OCR processing.

The script to generate this image is stored in **`scripts/generate_image.py`**.

### 🔹 Step 2: Splitting the Image
We don’t run OCR on the entire image at once. Instead, we split it into **4 overlapping regions** to increase detection accuracy. The regions are:
1. **Top-left** (extra width on the right, extra height on the bottom)
2. **Top-right** (extra width on the left, extra height on the bottom)
3. **Bottom-left** (extra width on the right, extra height on the top)
4. **Bottom-right** (extra width on the left, extra height on the top)

These **overlaps help capture words that might be cut off at the borders**.

### 🔹 Step 3: Running OCR
Each region is **sent to EasyOCR**, which returns:
- The **detected text** (e.g., "mango", "banana")
- The **bounding box coordinates** (where the word is in the image)
- The **confidence score** (how sure OCR is about the word)

### 🔹 Step 4: Why do we need NMS?
Because of the overlapping regions, **some words will be detected multiple times**! That’s where **Modified Non-Maximum Suppression (NMS)** comes in:
- It **sorts detections by confidence** (highest first).
- It **checks how much two bounding boxes overlap** using IOU (Intersection Over Union).
- If two detections are too close together (IOU > threshold), it **removes the lower-confidence one**.

This ensures we **only count each word once!**

### 🔹 Step 5: Visualizing Results
- The script **draws bounding boxes** around detected words.
- It **saves sub-images** of each region (`output_region_1.png`, etc.) with red lines marking the delta areas.
- A **final image (`output_detected.png`)** shows the cleaned-up results.

---


### 📸 Sample Output

#### **Generated Image with Random Words**
![output](https://github.com/user-attachments/assets/ba06af93-0163-4513-b4a4-54e5d1a45a87)


#### **Final Processed Image after OCR & NMS**
![output_detected](https://github.com/user-attachments/assets/1b1ff42d-09f9-4fd7-a6b4-1fded065bb6e)


---

## 🏃‍♂️ How to Run the Project
### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Generate the Image
```bash
python scripts/image_gen.py
```

### 3️⃣ Run the OCR + NMS Script
```bash
python scripts/nms.py --image data/image_gen.png
```

### 4️⃣ View Results
- Processed image: **`output_detected.png`**
- Split images: **`output_region_1.png`**, **`output_region_2.png`**, etc.

---

## 📂 Project Structure
```
OCR-Text-Detection-with-NMS/
├── data/                     # Store sample images here
├── output/                  # Save detected images here
├── scripts/                  # Python scripts
│   ├── nms.py             # Main detection script
│   ├── image_gen.py      # Script to create the image with random text
├── README.md                  # Explanation of project
├── requirements.txt           # Dependencies
├── .gitignore                 # Ignore unnecessary files
```

---

## 🎯 What’s Next?
- 🔍 **Tune the IOU threshold** to improve duplicate removal.
- 🚀 **Try different OCR models** for better accuracy.
- 🛠️ **Experiment with deltaW and deltaH** values.

Let me know if you try it out! Happy coding! 😃🎉

