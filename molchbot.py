import time

import utilities.color as clr
import utilities.random_util as rd
import utilities.imagesearch as imsearch
from model.bot import BotStatus
from model.zaros.zaros_bot import ZarosBot
from utilities.api.morg_http_client import MorgHTTPSocket
from utilities.api.status_socket import StatusSocket


import random


class ZarosMolchBot(ZarosBot):
    def __init__(self):
        bot_title = "Molch Bot"
        description = "Bots Molch Island aerial fishing."
        super().__init__(bot_title=bot_title, description=description)
        # Set option variables below (initial value is only used during UI-less testing)
        self.running_time = 1
        self.take_breaks = True

    def create_options(self):
        """
        Use the OptionsBuilder to define the options for the bot. For each function call below,
        we define the type of option we want to create, its key, a label for the option that the user will
        see, and the possible values the user can select. The key is used in the save_options function to
        unpack the dictionary of options after the user has selected them.
        """
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 240)
        self.options_builder.add_checkbox_option("take_breaks", "Take breaks?", [" "])


    def save_options(self, options: dict):
        """
        For each option in the dictionary, if it is an expected option, save the value as a property of the bot.
        If any unexpected options are found, log a warning. If an option is missing, set the options_set flag to
        False.
        """
        for option in options:
            if option == "running_time":
                self.running_time = options[option]
            elif option == "take_breaks":
                self.take_breaks = options[option] != []
            else:
                self.log_msg(f"Unknown option: {option}")
                print("Developer: ensure that the option keys are correct, and that options are being unpacked correctly.")
                self.options_set = False
                return
        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg(f"Bot will{' ' if self.take_breaks else ' not '}take breaks.")
        self.log_msg("Options set successfully.")
        self.options_set = True

    def main_loop(self):
        """
        When implementing this function, you have the following responsibilities:
        1. If you need to halt the bot from within this function, call `self.stop()`. You'll want to do this
           when the bot has made a mistake, gets stuck, or a condition is met that requires the bot to stop.
        2. Frequently call self.update_progress() and self.log_msg() to send information to the UI.
        3. At the end of the main loop, make sure to set the status to STOPPED.

        Additional notes:
        Make use of Bot/RuneLiteBot member functions. There are many functions to simplify various actions.
        Visit the Wiki for more.
        """
        # Setup APIs
        api_m = MorgHTTPSocket()
        api_s = StatusSocket()

        # Main loop
        self.log_msg("Selecting inventory...")
        self.mouse.move_to(self.win.cp_tabs[3].random_point())
        self.mouse.click()
    # These aren't necessary unless you need the script to read a specific chat.
    #    self.log_msg("Selecting game chat...")
    #    self.mouse.move_to(self.win.chat_tabs[0].random_point())
    #    self.mouse.click()
    #    self.mouse.move_to(self.win.chat_tabs[1].random_point())
    #    self.mouse.click()

        # Defines image search for knife and bluegill.

        #bluegill_img = imsearch.BOT_IMAGES.joinpath("items", "Bluegill.png")
        #knife_img = imsearch.BOT_IMAGES.joinpath("items", "knife.png")
        #knife := imsearch.search_img_in_rect(knife_img, self.win.control_panel)
        #bluegill := imsearch.search_img_in_rect(bluegill_img, self.win.control_panel)

        start_time = time.time()
        end_time = self.running_time * 60
        while time.time() - start_time < end_time:
            # -- Perform bot actions here --
            # 5% chance to take a break between clicks
            if rd.random_chance(probability=0.05) and self.take_breaks:
                self.take_break(max_seconds=23, fancy=True)

            if rd.random_chance(probability=.07):
                self.__fish_chunks()

# TODO: Optimize the fishing pool search so you don't run all over the fucking island.

            startfishes = self.get_all_tagged_in_rect(self.win.game_view, clr.CYAN)
            if startfishes:  # If there are fish pool in the game view
                fishes = self.get_all_tagged_in_rect(self.win.game_view, clr.CYAN)
                self.get_nearest_tag(clr.CYAN)
                self.log_msg("Fishing...")
                for fish in fishes:
                    self.get_nearest_tag(clr.CYAN)
                    self.mouse.move_to(fish.random_point())
                    if not self.mouseover_text(contains="Catch"):
                        continue
                    self.mouse.click()
                    time.sleep(random.uniform(2.8,3.2))



        self.update_progress((time.time() - start_time) / end_time)

        self.update_progress(1)
        self.__logout("Finished.")


    def __logout(self, msg):
        self.log_msg(msg)
        self.logout()
        self.set_status(BotStatus.STOPPED)

    def __fish_chunks(self):
        self.log_msg("Cutting fish into chunks...")
## Make sure you have the .png's listed downloaded into the ./src/images/bot/items folder.
        knife_img = imsearch.BOT_IMAGES.joinpath("items", "Knife.png")
        bluegill_img = imsearch.BOT_IMAGES.joinpath("items", "Bluegill.png")
        commontench_img = imsearch.BOT_IMAGES.joinpath("items", "Commontench.png")
        mottledeel_img = imsearch.BOT_IMAGES.joinpath("items", "Mottledeel.png")
        greatersiren_img = imsearch.BOT_IMAGES.joinpath("items", "Greatersiren.png")
        if knife := imsearch.search_img_in_rect(knife_img, self.win.control_panel):
            while bluegill_inv := imsearch.search_img_in_rect(bluegill_img, self.win.control_panel):
                    self.mouse.move_to(knife.random_point())
                    if not self.mouseover_text(contains="Knife"):
                        continue
                    self.mouse.click()
                    self.mouse.move_to(bluegill_inv.random_point())
                    if not self.mouseover_text(contains="Knife"):
                        continue
                    self.mouse.click()
                    time.sleep(random.uniform(0.7,0.9))
            while mottledeel_inv := imsearch.search_img_in_rect(mottledeel_img, self.win.control_panel):
                    self.mouse.move_to(knife.random_point())
                    if not self.mouseover_text(contains="Knife"):
                        continue
                    self.mouse.click()
                    self.mouse.move_to(mottledeel_inv.random_point())
                    if not self.mouseover_text(contains="Knife"):
                        continue
                    self.mouse.click()
                    time.sleep(random.uniform(0.7,0.9))
            while commontench_inv := imsearch.search_img_in_rect(commontench_img, self.win.control_panel):
                    self.mouse.move_to(knife.random_point())
                    if not self.mouseover_text(contains="Knife"):
                        continue
                    self.mouse.click()
                    self.mouse.move_to(commontench_inv.random_point())
                    if not self.mouseover_text(contains="Knife"):
                        continue
                    self.mouse.click()
                    time.sleep(random.uniform(0.7,0.9))
            while greatersiren_inv := imsearch.search_img_in_rect(greatersiren_img, self.win.control_panel):
                    self.mouse.move_to(knife.random_point())
                    if not self.mouseover_text(contains="Knife"):
                        continue
                    self.mouse.click()
                    self.mouse.move_to(greatersiren_inv.random_point())
                    if not self.mouseover_text(contains="Knife"):
                        continue
                    self.mouse.click()
                    time.sleep(random.uniform(0.7,0.9))



