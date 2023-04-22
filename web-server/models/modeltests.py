import unittest
import scene
import cv2
import numpy as np
import os


class imageClassTest(unittest.TestCase):
    def setUp(self):
        self.image = scene.Image()
        self.image.drop()

    def test_save_data(self):
        return

    def test_load_data(self):
        return


class userManagerTest(unittest.TestCase):
    def setUp(self):  # fires before the test starts
        self.user_manager = scene.UserManager()
        self.user_manager.collection.drop()

    def test_add_user(self):
        user = scene.User("me", "pass123", "1234")
        self.user_manager.set_user(user)

        user2 = scene.User("Jack Ryan", "qwerty", "12345")
        self.user_manager.set_user(user2)

        user3 = scene.User(
            "Jack Ryan", "pass123", "43279"
        )  # has same username as user2

        user4 = scene.User("Theodore K.", "letmein", "1234")  # has same id as user1

        ret = self.user_manager.get_user_by_id(user._id)

        print("User == " + str(user))
        print("User2 == " + str(user2))
        print("User returned from mongodb == " + str(ret))

        errorcode = self.set_user(user3)

        exceptionRaised = False

        try:  # should raise an exception because it has the same id
            self.user_manager.set_user(user4)
        except:
            exceptionRaised = True

        self.assertTrue(exceptionRaised)

        self.assertTrue(ret.username == user.username)
        self.assertTrue(ret.password == user.password)
        self.assertTrue(ret._id == user._id)

        self.assertFalse(ret.username == user2.username)
        self.assertFalse(ret.password == user2.password)
        self.assertFalse(ret._id == user2._id)

    # def tearDown(self):                    #fires after the test is completed
    # self.user_manager.collection.drop()


# Generate Noise Video
def generateVideo():
    size = 720 * 16 // 9, 720
    duration = 2
    fps = 25
    # VideoWriter_fourcc is a function to specify the video codec to use, and in this case mp4v is the codec
    out = cv2.VideoWriter(
        "output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (size[1], size[0]), False
    )

    # Go through the frames of the video and write it to out
    for _ in range(fps * duration):
        data = np.random.randint(0, 256, size, dtype="uint8")
        out.write(data)

    return out


# Testing Suite for the Video class for scene
class videoManagerTest(unittest.TestCase):
    # initalize a scenemanager
    def setUp(self):
        self.user_video = scene.SceneManager()

    # actual test
    def test_videoTest(self):
        v = scene.Video()
        example_video = generateVideo()
        example_video.release()

        # save to local file system at the name "output.mp4"
        v.file_path = "output.mp4"

        # Try to load the data and see if it exists
        try:
            print("Data Loaded")
            v.load_data()
        except Exception as e:
            self.fail(f"an Error has occurred:{e}")

        self.assertIsNone(v.video_data)

        # check the video_data by matching with expected results
        print(v.video_data)
        print("Path Existed")
        # Lastly remove the file to ensure no residue is left behind
        if os.path.exists("output.mp4"):
            os.remove("output.mp4")
            print("File Removed Success")
        else:
            self.fail("File does not exist")

    def test_toDictTest(self):
        def test_to_dict(self):
            # creating a new video object
            example_video = generateVideo()
            example_video.release()

            o_file_path = "output.mp4"

            # Video object that is made with all of the parameters
            video = scene.Video(
                file_path=o_file_path,
                width=720 * 16 // 9,
                height=720,
                fps=25,
                duration=2,
            )

            # What we expect the video object to contain
            expected_dict = {
                "file_path": "output.mp4",
                "width": 720 * 16 // 9,
                "height": 720,
                "fps": 25,
                "duration": 2,
            }

            self.assertEqual(video.to_dict, expected_dict)

            self.assertEqual(dict(video), expected_dict)

            if os.path.exists("output.mp4"):
                os.remove("output.mp4")
                print("File Removed Success")
            else:
                self.fail("File does not exist")

        return

    def test_fromDictTest(self):
        # creating a new video object
        example_video = generateVideo()
        example_video.release()

        # The dictionary with all of the values
        this_dict = {
            "file_path": "output.mp4",
            "width": 720 * 16 // 9,
            "height": 720,
            "fps": 25,
            "duration": 2,
        }

        # Constructing a new video object and using from_dict to populate the attributes
        preconstructed_video = scene.Video()
        preconstructed_video.from_dict(this_dict)

        o_file_path = "output.mp4"

        # The object that from_dict should make with the video class
        finished_video = scene.Video(
            file_path=o_file_path,
            width=720 * 16 // 9,
            height=720,
            fps=25,
            duration=2,
        )

        self.assertEquals(preconstructed_video.to_dict, finished_video.to_dict)

        if os.path.exists("output.mp4"):
            os.remove("output.mp4")
            print("File Removed Success")
        else:
            self.fail("File does not exist")


if __name__ == "__main__":
    unittest.main()
