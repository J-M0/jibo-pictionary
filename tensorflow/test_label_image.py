import tensorflow as tf, sys, os, re

count = 0
TEST_PATH = "/TF_M_FILES/TestingDataSet5/test_set_5/"
tot_count = len(os.listdir(TEST_PATH))-1
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("/TF_M_FILES/retrained_labels.txt")]
with tf.gfile.FastGFile("/TF_M_FILES/retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
    # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

    for image_path in os.listdir(TEST_PATH):
        if not image_path.startswith('.'):
            print "PROCESSING "+ image_path
            # Read in the image_data
            image_data = tf.gfile.FastGFile(TEST_PATH+image_path, 'rb').read()

            
                
            predictions = sess.run(softmax_tensor, \
                     {'DecodeJpeg/contents:0': image_data})

                
                # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            
            node_id = top_k[0]
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print('File name = %s Label Classified = "%s" (score = %.5f)' % (image_path, human_string, score))
            if(re.findall(label_lines[node_id], image_path, re.I)):
                count +=1;
#print count, tot_count
print ((float(count))/tot_count)*100
