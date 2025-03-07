import cv2
import numpy as np
import easyocr
from PIL import Image

def iou(box1, box2):
    """Calculate Intersection over Union (IOU) between two bounding boxes."""
    x1, y1, x2, y2 = box1
    x1g, y1g, x2g, y2g = box2
    xi1 = max(x1, x1g)
    yi1 = max(y1, y1g)
    xi2 = min(x2, x2g)
    yi2 = min(y2, y2g)
    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x2g - x1g) * (y2g - y1g)
    union_area = box1_area + box2_area - inter_area
    return inter_area / union_area if union_area else 0

def modified_nms(detections, threshold=0.5):
    """Applies Non-Maximum Suppression to remove duplicate text detections."""
    detections = sorted(detections, key=lambda x: x[2], reverse=True)  # Sort by confidence
    final_detections = []
    while detections:
        best = detections.pop(0)
        final_detections.append(best)
        detections = [d for d in detections if iou(best[1], d[1]) < threshold]
    return final_detections

def detect_text(image_path, deltaH=50, deltaW=50, visualize=False):
    """Detects text in an image using EasyOCR, applies MNS for filtering, and saves the visualization."""
    reader = easyocr.Reader(['en'])
    image = cv2.imread(image_path)
    h, w, _ = image.shape
    
    # Define 4 overlapping sub-regions
    regions = [
        (0, 0, w//2 + deltaW, h//2 + deltaH),  # Top-left (delta on right & bottom)
        (w//2 - deltaW, 0, w, h//2 + deltaH),  # Top-right (delta on left & bottom)
        (0, h//2 - deltaH, w//2 + deltaW, h),  # Bottom-left (delta on right & top)
        (w//2 - deltaW, h//2 - deltaH, w, h)   # Bottom-right (delta on left & top)
    ]
    
    all_detections = []
    for i, (x1, y1, x2, y2) in enumerate(regions):
        sub_img = image[y1:y2, x1:x2].copy()
        
        # Draw deltaH and deltaW lines selectively
        if i == 0:  # Top-left
            cv2.line(sub_img, (x2 - x1 - deltaW, 0), (x2 - x1 - deltaW, y2 - y1), (255, 0, 0), 2)  # Right boundary
            cv2.line(sub_img, (0, y2 - y1 - deltaH), (x2 - x1, y2 - y1 - deltaH), (255, 0, 0), 2)  # Bottom boundary
        elif i == 1:  # Top-right
            cv2.line(sub_img, (deltaW, 0), (deltaW, y2 - y1), (255, 0, 0), 2)  # Left boundary
            cv2.line(sub_img, (0, y2 - y1 - deltaH), (x2 - x1, y2 - y1 - deltaH), (255, 0, 0), 2)  # Bottom boundary
        elif i == 2:  # Bottom-left
            cv2.line(sub_img, (x2 - x1 - deltaW, 0), (x2 - x1 - deltaW, y2 - y1), (255, 0, 0), 2)  # Right boundary
            cv2.line(sub_img, (0, deltaH), (x2 - x1, deltaH), (255, 0, 0), 2)  # Top boundary
        elif i == 3:  # Bottom-right
            cv2.line(sub_img, (deltaW, 0), (deltaW, y2 - y1), (255, 0, 0), 2)  # Left boundary
            cv2.line(sub_img, (0, deltaH), (x2 - x1, deltaH), (255, 0, 0), 2)  # Top boundary
        
        results = reader.readtext(sub_img, width_ths= 0.3)
        for (bbox, text, conf) in results:
            (xA, yA), (xB, yB) = bbox[0], bbox[2]
            all_detections.append((text.lower(), (xA+x1, yA+y1, xB+x1, yB+y1), conf))
            
            # Draw bounding boxes for visualization
            cv2.rectangle(sub_img, (xA, yA), (xB, yB), (0, 255, 0), 2)
            cv2.putText(sub_img, text, (xA, yA - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Save sub-image with detections
        cv2.imwrite(f"output_region_{i+1}.png", sub_img)
    
    # Apply MNS to remove duplicate detections
    filtered_detections = modified_nms(all_detections)
    
    # Count occurrences of each fruit word
    fruits = {"mango": 0, "banana": 0, "strawberry": 0, "orange": 0}
    for text, bbox, _ in filtered_detections:
        if text in fruits:
            fruits[text] += 1
            
        # Draw bounding boxes if visualization is enabled
        if visualize:
            x1, y1, x2, y2 = bbox
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    if visualize:
        output_path = "output_detected.png"
        cv2.imwrite(output_path, image)
        print(f"Visualization saved at: {output_path}")
        print("Sub-region visualizations saved as output_region_1.png to output_region_4.png")
    
    return fruits

# Example usage
image_path = r"C:\Thesis\Dataprep\output\output.png"  # Update with actual path
fruit_counts = detect_text(image_path, visualize=True)
print("Final word counts after NMS:", fruit_counts)

