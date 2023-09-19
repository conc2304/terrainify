import maya.cmds as cmds
import constants


class BPM_Service:
    def __init__(self):
        self.start_frame = 10
        self.end_frame: int = None
        self.total_frames: int = None
        self.bpm: int = None
        self.bars: int = None
        self.fps: int = None
        self.loops: int = None

    def get_current_fps_setting(self):
        # Get the current time unit (FPS setting)
        time_unit = cmds.currentUnit(query=True, time=True)
        print(time_unit)

        # Convert the time unit to a numeric FPS value
        fps_value = constants.fps_mapping.get(time_unit, None)

        print("Current FPS:", fps_value)
        self.fps = fps_value
        return fps_value

    def get_animation_frame_range(self, bpm, num_bars):
        # Get the animation start and end points based on bpm and total bars
        fps = self.get_current_fps_setting()

        frames_per_beat = (60.0 / bpm) * fps
        beats_per_bar = 4
        total_frames = frames_per_beat * beats_per_bar * num_bars

        end_frame = self.start_frame + total_frames

        self.end_frame = end_frame
        self.total_frames = total_frames

        print(f"TOTAL FRAMES: {self.total_frames}")

        return {
            "start": self.start_frame,
            "end": end_frame,
            "total": total_frames,
        }

    def set_playback_options(self, start=None, end=None):
        # If a value was passed in use that, if not use what is saved internally
        if start == None or end == None:
            if self.start_frame == None or self.end_frame == None:
                return

            start_frame = self.start_frame
            end_frame = self.end_frame
        else:
            start_frame = start
            end_frame = end

        # Focus the playback widget to our used ranges
        cmds.playbackOptions(
            minTime=start_frame,
            maxTime=end_frame,
            animationStartTime=start_frame,
            animationEndTime=end_frame,
        )

    def animate_object_on_downbeat(
        self,
        object_name,
        attribute_name,
        bpm,
        num_bars,
        beat_start_val,
        beat_end_val,
        anim_beat_length,
    ):
        # Calculate the frames per beat
        self.get_animation_frame_range(bpm, num_bars)

        fps = self.get_current_fps_setting()
        frames_per_beat = (60.0 / bpm) * fps
        beat_per_bar = 4

        # Keep internal state up to date
        self.bars = num_bars
        self.bpm = bpm

        # Set key frames for the start and end of the animated beat
        for bar in range(int(num_bars)):
            frame = self.start_frame + int(bar * beat_per_bar * frames_per_beat)
            cmds.setKeyframe(
                object_name, attribute=attribute_name, value=beat_start_val, time=frame
            )
            cmds.setKeyframe(
                object_name,
                attribute=attribute_name,
                value=beat_end_val,
                time=frame + frames_per_beat * anim_beat_length,
            )
            # Set animation tangents to linear
            cmds.keyTangent(
                object_name,
                attribute=attribute_name,
                time=(frame, frame + frames_per_beat),
                ott="linear",
                itt="linear",
            )

    def animate_object_on_loop(
        self, object_name, attribute_name, bpm, num_bars, loops, start_val, end_val
    ):
        # Get the length of the full clip based on frame rate, bpm and number of bar
        frame_range = self.get_animation_frame_range(bpm, num_bars)
        total_frames = frame_range["total"]

        loop_step = total_frames / loops
        loop_values = [start_val, end_val]

        print(f"Total Frames: {total_frames}")
        print(f"Total Loops: {loops}")
        print(f"Loop Step: {loop_step}")

        # Add animiation frames
        for frame in range(
            int(self.start_frame), int(frame_range["end"]), int(loop_step)
        ):
            loop_index = (frame // int(loop_step)) % 2
            print(f"Frame {frame}")
            print(f"Loop Index {loop_index}")

            cmds.setKeyframe(
                object_name,
                attribute=attribute_name,
                value=loop_values[loop_index],
                time=frame,
            )
            if frame != total_frames:
                cmds.keyTangent(
                    object_name,
                    attribute=attribute_name,
                    time=(frame, frame + int(loop_step)),
                    itt="linear",
                    ott="linear",
                )

    def animate_rotation(
        self, object_name, attribute_name, num_bars, num_loops=0, bpm=120
    ):
        print("Animate Rotation")
        # For rotation we are adding and not looping
        frame_range = self.get_animation_frame_range(bpm, num_bars)
        total_frames = frame_range["total"]
        start_frame = frame_range["start"]

        self.bpm = bpm
        self.loops = num_loops
        self.bars = num_bars

        print(f"Start: {start_frame}, Total: {total_frames}")

        # Calculate rotation step for each quarter rotation to match 4/4 time signature
        rotation_per_loop = 360.0
        total_rotation = num_loops * rotation_per_loop
        quarter_rotation_frames = total_frames // (num_loops * 4)

        # Set rotation keyframes for every quarter rotation
        total_quarter_turns = num_loops * 4
        for loop in range(1 + total_quarter_turns):
            frame = int(start_frame) + loop * quarter_rotation_frames
            rotation_value = loop * (rotation_per_loop / 4)
            cmds.setKeyframe(
                object_name, attribute=attribute_name, value=rotation_value, time=frame
            )

            # Set the easing of the key tangents to linear
            if loop < total_quarter_turns:
                next_frame = (loop + 1) * quarter_rotation_frames + start_frame
                cmds.keyTangent(
                    object_name,
                    attribute=attribute_name,
                    time=(frame, next_frame),
                    itt="linear",
                    ott="linear",
                )

            if loop == total_quarter_turns:
                cmds.keyTangent(
                    object_name,
                    attribute=attribute_name,
                    time=(frame, frame),
                    itt="linear",
                    ott="linear",
                )
