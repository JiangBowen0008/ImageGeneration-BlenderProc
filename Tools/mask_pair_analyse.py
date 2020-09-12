import json
import os
import cv2
import math
import numpy as np
from sklearn.preprocessing import normalize


def get_mask_centroid(mask):

    # get mask contours
    contours, _ = cv2.findContours( mask,
                                    cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_SIMPLE)
    maxIdx = -1
    maxArea = 0
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > maxArea:
            maxIdx = i
            maxArea = area
    
    if maxIdx == -1:
        return None

    contour_max = contours[maxIdx]
    # calculate centroid of contours
    M = cv2.moments(contour_max)
    c_x = int(M["m10"] / M["m00"])
    c_y = int(M["m01"] / M["m00"])

    centroid = [c_x, c_y]
    return centroid


def get_mask_area(mask_image):
    mask_pixel_value = mask_image[mask_image > 0.1]
    mask_area = len(mask_pixel_value)
    return mask_area


def get_visible_rate(mask_image, mask_visible_image):
    # get number of occluded pixel
    occlude_area = mask_image - mask_visible_image
    occlude_pixel_value = mask_image[occlude_area > 0.1]
    num_occluded = len(occlude_pixel_value)

    mask_area = get_mask_area(mask_image)
    visible_rate = 1 - (num_occluded / mask_area)
    return visible_rate

def get_distance(target, mid_point):
    # calculate the distance between the target and the midpoint
    x_diff = target[0] - mid_point[0]
    y_diff = target[1] - mid_point[1]
    distance = math.hypot(x_diff, y_diff)
    return distance

def range_normalize(list):
    list = np.array(list)
    min_data = np.min(list, axis = 1)
    max_data = np.max(list, axis = 1)
    data_range = (max_data - min_data)
    norm_data = (list - min_data[:, None]) / data_range[:, None]
    return norm_data

def std_normalize(list):
    list = np.array(list)
    avg_data = np.mean(list, axis = 1)
    var_data = np.var(list, axis = 1)
    norm_data = (list - avg_data[:, None]) / var_data[:, None]
    return norm_data

def main():
    # data directory
    data_dir = '../output/bop_data/lmo/train_pbr'
    image_dir = os.listdir(data_dir)
    threshold = 20

    for sub_file in image_dir:
        if os.path.isdir(os.path.join(data_dir, sub_file)):
            scene_gt_path = os.path.join(data_dir, sub_file, 'scene_gt.json')

            with open(scene_gt_path, 'r') as f:
                data = json.load(f)
                scores = {}

                for i in data:
                    scene_key = str(i)
                    scene = data[scene_key]
                    scores[scene_key] = {}

                    centroid_distance_grasp = []
                    centroid_distance_suction = []
                    visible_rate_list = []
                    reciprocal_mask_area_list = []
                    mask_visible_area_list = []
                    mask_name_list = []
                    centroid_x_list = []

                    for j, obj in enumerate(scene):
                        # get mask and depth image name
                        scene_id = "{:0>6d}".format(int(i))
                        mask_id = "{:0>6d}".format(int(j))
                        mask_name = "{}_{}.png".format(scene_id, mask_id)
                        depth_name = "{}.png".format(scene_id)

                        # grasp score
                        # grasp_score = distance to right midpoint + visible rate/mask area
                        right_midpoint = [215, 520]
                        left_midpoint = [200, 20]

                        # load mask
                        mask_path = os.path.join(data_dir, sub_file, 'mask', mask_name)
                        mask_visible_path = os.path.join(data_dir, sub_file, 'mask_visib', mask_name)

                        mask_image = cv2.imread(mask_path,
                                                cv2.IMREAD_GRAYSCALE)
                        mask_visible_image = cv2.imread(mask_visible_path,
                                                        cv2.IMREAD_GRAYSCALE)

                        # cv2.imshow("mask image", mask_image)
                        # cv2.imshow("mask visible image", mask_visible_image)
                        # cv2.waitKey(0)

                        # get centroid of mask
                        visible_mask_centroid = get_mask_centroid(mask_visible_image)
                        if visible_mask_centroid == None:
                            continue

                        centroid_x = visible_mask_centroid[0]

                        # distance between visible mask centroid and midpoints
                        distance_2_right_midpoint = get_distance(visible_mask_centroid, right_midpoint)
                        distance_2_lift_midpoint = get_distance(visible_mask_centroid, left_midpoint)

                        # get visible rate
                        visible_rate = get_visible_rate(mask_image, mask_visible_image)

                        # get area of mask
                        reciprocal_mask_area = 1.0 / get_mask_area(mask_image)

                        # suction score
                        # suction_score = distance to lift midpoint + visible area
                        mask_visible_area = get_mask_area(mask_visible_image)                        

                        centroid_distance_grasp.append(distance_2_right_midpoint)
                        centroid_distance_suction.append(distance_2_lift_midpoint)
                        visible_rate_list.append(visible_rate)
                        reciprocal_mask_area_list.append(reciprocal_mask_area)
                        mask_visible_area_list.append(mask_visible_area)
                        mask_name_list.append(mask_name)
                        centroid_x_list.append(centroid_x)

                    # converting mask names to numpy array for later processing
                    mask_name_list = np.array(mask_name_list)

                    # normalize
                    featureList = np.array([centroid_distance_grasp,
                                            centroid_distance_suction,
                                            visible_rate_list,
                                            reciprocal_mask_area_list,
                                            mask_visible_area_list]).transpose()
                    print(featureList.shape)
                    norm_feat = range_normalize(featureList)

                    # calculating score
                    suction_score = np.mean(norm_feat[:, [1, 4]], axis = 1)
                    grasp_score = np.mean(norm_feat[:, [0, 2, 3]], axis = 1)

                    
                    # pair-wise analysis
                    # i points to the left object (suction)
                    # j points to the right object (grasp)
                    suction_name_idx = []
                    grasp_name_idx = []
                    num_obj = mask_name_list.shape[0]
                    for i in range(num_obj):
                        for j in range(num_obj):

                            # skip when two objects are the same
                            if i == j:
                                continue

                            # skip for overlapping arms
                            if centroid_x_list[j] - centroid_x_list[i] < threshold:
                                continue

                            # calculating the combination score
                            suction_name_idx.append(i)
                            grasp_name_idx.append(j)

                    # calculating scores
                    comb_suction_score = suction_score[suction_name_idx]
                    comb_grasp_score = grasp_score[grasp_name_idx]
                    comb_score = comb_suction_score + comb_grasp_score
                    idx = np.array(np.argsort(-comb_score))
                    ranked_comb_score = comb_score[idx]

                    # getting corresponding ranked names
                    suction_name = mask_name_list[suction_name_idx]
                    grasp_name = mask_name_list[grasp_name_idx]
                    ranked_suction_name = suction_name[idx]
                    ranked_grasp_name = grasp_name[idx]
                    ranked_comb_names = list(zip(ranked_suction_name, ranked_grasp_name))

                    # storing inside the scene dictionary
                    scores[scene_key]["comb_score"] = ranked_comb_score.tolist()
                    scores[scene_key]["comb_names"] = ranked_comb_names
                
                # store the scores
                scores_path = os.path.join(data_dir, sub_file, 'scene_score.json')
                with open(scores_path, 'w') as outfile:
                    json.dump(scores, outfile, indent=2, sort_keys=True)
                
                    

if __name__ == '__main__':
    main()