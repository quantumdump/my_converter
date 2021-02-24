import os, shutil
import stat

#creating switch statement for resolution
def switch_resolution(resolution_name):
    switcher = {

    #Set 
    	#720p
        '720p':'1280x720',
        #1080p
        '1080p':'1920x1080',
        #4k
        '4k':'3840x2160'

        }
    return switcher.get(resolution_name, "There\'s no such resolution")

#fn to change video resolution of given video file
def change_resolution(video_file, resolution_name, output_folder, output_filename, subdir):
	#Create same folders as in in_folder if needed
	folders_tree_list = subdir.split('\\')
	print('Folders tree:', folders_tree_list)
	#Delete first folder from list
	folders_tree_list.pop(0)
	print('New Folders Tree list:', folders_tree_list)
	#Convert back to path
	the_subdir = '/'.join(folders_tree_list)
	print('THE SUBODIR IS:', the_subdir, '-end')
	#If folder(s) doesn't exist in output folder, create
	if not os.path.exists(the_subdir):
		os.makedirs(r''+output_folder+'/'+the_subdir)
	print('Changing resolution of ', video_file, ' to ', resolution_name)

	#get resolution width x height from "switch_resolution" function
	resolution_w_h = switch_resolution(resolution_name)

	#set ffmpeg command for command line
	ffmpeg_command = 'ffmpeg -i ' + video_file + ' -c:v libx264 -crf 20 -preset slow' + ' -c:a copy -s '+ resolution_w_h + ' ' +output_folder + '/'+ the_subdir +'/'+ output_filename
	os.system(ffmpeg_command)
#Set In and Out folders
in_folder = 'files_to_convert'
out_folder = 'output_files'

#Iterate through folder tree
for subdir, dirs, files in os.walk(r''+in_folder):
    for filename in files:
    	#Full filepath
        filepath = subdir + os.sep + filename
        print('Subdir is ', subdir)
        #if file is video
        if filepath.endswith(".MP4") or filepath.endswith(".mkv"):

            print ('Filepath is: ', filepath)

            change_resolution(filepath, '1080p', out_folder, filename, subdir)

#Delete all files in 'delete_list'
os.chdir(in_folder)
os.system('DEL /F/Q/S *.* > NUL')
#Delete empty folders
os.chdir('..')

def rec_rmdir(root, callback, preserve=True):
    for path in (os.path.join(root, p) for p in os.listdir(root)):
        st = os.stat(path)
        if stat.S_ISREG(st.st_mode):
            callback(path)
        elif stat.S_ISDIR(st.st_mode):
            rec_rmdir(path, callback, preserve=False)
    if not preserve:
        try:
        #remove empty dir...
            print('Removing empty folders...')
            os.rmdir(root)
        except IOError:
            pass
def process_file_and_remove(path):
    # process the file
    # ...
    os.remove(path)
rec_rmdir(in_folder, process_file_and_remove)