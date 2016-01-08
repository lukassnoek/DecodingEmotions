# --- Blocked/event-related: PICTURES (task 2) --- #

# To do:
# - fMRI knoppenkast/buttons
# - Juiste welkomstekst
# - Juiste Cue-tekst

# ------------------------------ SDL headers ------------------------------ #

default_background_color = 0,0,0;
response_matching = simple_matching;
default_font_size = 20;
default_font = "arial";
active_buttons = 4;
button_codes = 1,2,3,4;

#scenario_type = fMRI_emulation;
#scan_period = 2000;
response_logging = log_all;
no_logfile = false;   

# ------------------------------ SDL definitions: TEXT objects ------------------------------ #
# ------------------------------------------------------------------------------------------- #

begin;

# Introduction text (example)
text {
			caption = 	"Je gaat nu beginnen met de HOE, WAT en WAAROM taak.

Bij de cue HOE identificeer je expressies in het gezicht of lichaam 
die informatief zijn over de toestand waar de persoon zich in bevindt. 

Bij de cue WAT identificeer je sensaties in het lichaam die de persoon 
in die situatie zou kunnen ervaren.

Bij de cue WAAROM identificeer je een specifieke reden die verklaart 
waarom de persoon de emotie beleeft.

Druk op één van de response knoppen om met de taak te beginnen."; 
			font =		"arial";		
			font_size = 16;
			
} introduction;

# Fixation (NOT USED ANYMORE)
# text {caption = "+";} fix;

# Pause (for in between blocks) (NOT USED ANYMORE)
# text {caption = "Pauze";} pause;

# Cues
text {caption = "HOE?";} cue_how;
text {caption = "WAT?";} cue_what;
text {caption = "WAAROM?";} cue_why;

# Ending
text {
			caption = 	"Dit is het einde van dit deel van het experiment."; 
} end;

# ------------------------------ SDL definitions: BITMAP objects ------------------------------ #

# Experimental bitmap
bitmap {
			filename = "";
			preload = false;
} exp_bitmap;

# ------------------------------ SDL definitions: PICTURES ------------------------------ #

# Default picture (used for ITI, NULL-trial, and PAUSE-trial)
picture {background_color = 0,0,0;} default_picture;

# Fix (NOT USED ANYMORE)
# picture {text fix; x = 0; y = 0;} fix_picture;

# Intro
picture {text introduction; x = 0; y = 0;} introduction_picture;

# Wacht op eerste ttl pulse
picture {text { caption = "Wacht op eerste pulse"; font="arial"; font_size = 16;}; x=-60; y=0;} pulsetrial;

# End
picture {text end; x = 0; y = 0;} end_picture;

# Experimental picture
picture {bitmap exp_bitmap; x = 0; y = 0;} experimental_picture;

# Pause picture (for in between blocks) (NOT USED ANYMORE)
# picture {text pause; x = 0; y = 0;} pause_picture;

# Cues (instructions per block)
picture {text cue_how; x = 0; y = 0;} cue_how_picture;
picture {text cue_what; x = 0; y = 0;} cue_what_picture;
picture {text cue_why; x = 0; y = 0;} cue_why_picture;

# ------------------------------ SDL definitions: TRIALS ------------------------------ #

# Intro trial
trial {
	all_responses		= true; 
	trial_type 			= first_response;
	trial_duration 	= forever;
	stimulus_event {picture introduction_picture; time = 0;} introduction_event;
} introduction_trial;

# Experimental trial: Picture 
trial {
	stimulus_event {
		picture experimental_picture;
		duration = 6000; 
	} experimental_event;
} experimental_trial; 

# Pause-trial (between blocks)
# trial {
#	stimulus_event {
#		picture pause_picture;
#		duration = 3000;
#	} pause_event;
#} pause_trial;

# NULL-trial (in PCL, an extra ITI of 2000 sec is added; adjusted by clocktime)
# trial {
#	stimulus_event {
#		picture ITI_picture;
#		duration = 8000;
#	} null_event;
#} null_trial;

# End trial
trial {
	stimulus_event {
		picture end_picture;
		duration = 2000;
	} end_event;
} end_trial;

# Cue trials
trial {
	stimulus_event {
		picture cue_how_picture;
		duration = 4000;
	} cue_how_event;
} cue_how_trial; # CUE: HOW (action)

trial {
	stimulus_event {
		picture cue_what_picture;
		duration = 4000;
	} cue_what_event;
} cue_what_trial; # CUE: WHAT (interoception)

trial {
	stimulus_event {
		picture cue_why_picture;
		duration = 4000;
	} cue_why_event;
} cue_why_trial; # CUE: WHY (situation)

# ------------------------------ START OF PCL ------------------------------ #
# -------------------------------------------------------------------------- #
begin_pcl;

# Regular execution of intro trial and pulsetrial
introduction_trial.present();

pulsetrial.present();
int currentpulse_count=pulse_manager.main_pulse_count();
loop until pulse_manager.main_pulse_count()-currentpulse_count>1 begin                   #waits for a pulse and shows instructions
end;

# ------------------------------ Stimuli arrays ------------------------------ #
# Three arrays with the same stimuli (just 10 for now; should be 30)
						
# Block: how		
array <string> pic_how[30] =			
 {	"001.jpg", "002.jpg", "003.jpg", "004.jpg", "005.jpg", "006.jpg", "007.jpg", "008.jpg", "009.jpg", "010.jpg",
   "011.jpg", "012.jpg", "013.jpg", "014.jpg", "015.jpg", "016.jpg", "017.jpg", "018.jpg", "019.jpg", "020.jpg",
	"021.jpg", "022.jpg", "023.jpg", "024.jpg", "025.jpg", "026.jpg", "027.jpg", "028.jpg", "029.jpg", "030.jpg",
};

#Block: what
array <string> pic_what[30] =			
 {	"001.jpg", "002.jpg", "003.jpg", "004.jpg", "005.jpg", "006.jpg", "007.jpg", "008.jpg", "009.jpg", "010.jpg",
   "011.jpg", "012.jpg", "013.jpg", "014.jpg", "015.jpg", "016.jpg", "017.jpg", "018.jpg", "019.jpg", "020.jpg",
	"021.jpg", "022.jpg", "023.jpg", "024.jpg", "025.jpg", "026.jpg", "027.jpg", "028.jpg", "029.jpg", "030.jpg",
};

#Block: why
array <string> pic_why[30] =			
 {	"001.jpg", "002.jpg", "003.jpg", "004.jpg", "005.jpg", "006.jpg", "007.jpg", "008.jpg", "009.jpg", "010.jpg",
   "011.jpg", "012.jpg", "013.jpg", "014.jpg", "015.jpg", "016.jpg", "017.jpg", "018.jpg", "019.jpg", "020.jpg",
	"021.jpg", "022.jpg", "023.jpg", "024.jpg", "025.jpg", "026.jpg", "027.jpg", "028.jpg", "029.jpg", "030.jpg",
};

# ------------------------------ Condition-array ------------------------------ #
# Block-condition (how, what, why) 

array <int> block_condition[18] =
 { 1, 1, 1, 1, 1, 1,
	2, 2, 2, 2, 2, 2,
	3, 3, 3, 3, 3, 3,
}; # 1 = how, 2 = what, 3 = why

block_condition.shuffle();					#Randomization


# ------------------------------ Index-arrays ------------------------------ #
# Three index-arrays for 3 different blocks (randomized)

# Block: how
array <int> index_how[30] =
 { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,};

index_how.shuffle();						
 
# Block: what
array <int> index_what[30] =
 { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,};

index_what.shuffle();			

# Block: why 
array <int> index_why[30] =
 { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,};

index_why.shuffle();					

# ------------------------------ Iteration variables ------------------------------ #

# Iteration variables of stimuli (per condition): keeps track of presented stimuli per condition
int iteration_how = 0;
int iteration_what = 0;
int iteration_why = 0;

# Timing variables (for clocktime() loops)
int start_pic = 0;	
int start_null = 0;
int start_pause = 0;

# ------------------------------ START: LOOP FOR BLOCKS -------------------------------- #
# -------------------------------------------------------------------------------------- #	
loop int i = 1 until i > block_condition.count() begin;

	int block_draw = block_condition[i]; 	# random condition is drawn
	int null_position = random(2,6);			# random null_position is generated
	
	# Block == HOW
	if (block_draw == 1) then
		cue_how_event.set_event_code("Cue How");
		cue_how_trial.present();
		
		# ------------------------------ START: LOOP FOR WITHIN "HOW" ------------------------------ #
		
		# Six stimuli are presented in succession (incl. NULL)
		loop int j = 1 until j > 6 begin;
		
			# Presentation NULL-trial
			if (null_position == j) then
				start_null = clock.time();
				default_picture.present();
				logfile.add_event_entry("NULL");
				loop until clock.time() > (start_null+10000) begin end;
			
			# Presentation regular stimulus (picture)
			else
				start_pic = clock.time();
				iteration_how = iteration_how + 1;
				
				exp_bitmap.unload();
				exp_bitmap.set_filename(pic_how[index_how[iteration_how]]);
				exp_bitmap.load();
				experimental_event.set_event_code(string(index_how[iteration_how]+100));
				experimental_trial.present();
				default_picture.present();
				logfile.add_event_entry("ITI");
				loop until clock.time() > (start_pic+6000+2000) begin end;
			
			end;
			
			j = j + 1;
			
		end;
		# ------------------------------ END: LOOP FOR WITHIN "HOW" ------------------------------ #
	
	# Block == WHAT
	elseif (block_draw == 2) then
		cue_what_event.set_event_code("Cue What");
		cue_what_trial.present();
		
		# ------------------------------ START: LOOP FOR WITHIN "WHAT" ------------------------------ #
		
		# Six stimuli are presented in succesion (incl. NULL)
		loop int j = 1 until j > 6 begin;
		
			# Presentation NULL-trial
			if (null_position == j) then
				start_null = clock.time();
				default_picture.present();
				logfile.add_event_entry("NULL");
				loop until clock.time() > (start_null+10000) begin end;
				
			#Presentation regular stimulus
			else
				start_pic = clock.time();
				iteration_what = iteration_what + 1;
				
				exp_bitmap.unload();
				exp_bitmap.set_filename(pic_what[index_what[iteration_what]]);
				exp_bitmap.load();
				experimental_event.set_event_code(string(index_what[iteration_what]+200));
				experimental_trial.present();
				default_picture.present();
				logfile.add_event_entry("ITI");
				loop until clock.time() > (start_pic+6000+2000) begin end;
			
			end;
			
			j = j + 1;
			
		end;
		# ------------------------------ END: LOOP FOR WITHIN "WHAT" ------------------------------ #
	
	
	# Block == WHY
	elseif (block_draw == 3) then
		cue_why_event.set_event_code("Cue Why");
		cue_why_trial.present();
		
		# ------------------------------ START: LOOP FOR WITHIN "WHY" ------------------------------ #
		
		# Six stimuli are presented in succesion (incl. NULL)
		loop int j = 1 until j > 6 begin;
		
			# Presentation of NULL-trial
			if (null_position == j) then
				start_null = clock.time();
				default_picture.present();
				logfile.add_event_entry("NULL");
				loop until clock.time() > (start_null+10000) begin end;
				
			# Presentation of regular stimulus
			else
				start_pic = clock.time();
				iteration_why = iteration_why + 1;
				exp_bitmap.unload();
				exp_bitmap.set_filename(pic_why[index_why[iteration_why]]);
				exp_bitmap.load();
				experimental_event.set_event_code(string(index_why[iteration_why]+300));
				experimental_trial.present();
				default_picture.present();
				logfile.add_event_entry("ITI");
				loop until clock.time() > (start_pic+6000+2000) begin end;
			
			end;
			
			j = j + 1;
			
		end;
		# ------------------------------ END: LOOP FOR WITHIN "WHY" ------------------------------ #
			
	end; #end of if-statement of block-condition
	
	start_pause = clock.time();
	
	# Pause trial
	default.present();
	logfile.add_event_entry("pause");
	loop until clock.time() > (start_pause+4000) begin end;
	
	i = i + 1;
	
end; 
# ------------------------------ END: LOOP FOR BLOCKS -------------------------------- #
# ------------------------------------------------------------------------------------ #
end_event.set_event_code("END");
end_trial.present();


