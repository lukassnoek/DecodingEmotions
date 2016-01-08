# --- Event-related runs: SENTENCES --- #

# --------------- SDL headers --------------- #

scenario_type = fMRI;
#scenario_type = fMRI_emulation;
#scan_period = 2000;
pulses_per_scan = 300;
pulse_code = 30;
default_background_color = 0,0,0;
response_matching = simple_matching;
default_font_size = 60;
active_buttons = 4;
button_codes = 1,2,3,4;
response_logging = log_all;
no_logfile = false;   

begin; 

# --------------- SDL definitions: TEXT objects --------------- #

# Introduction text (example)
text {
			caption = 	"Je gaat nu de taak uitvoeren waarin je de inhoud van zinnen gaat voorstellen. 
Sommige zinnen beschrijven acties en expressies. Het is dan de bedoeling dat je je voorstelt dat jij 
deze actie of expressie uitvoert. Andere zinnen beschrijven sensaties of gevoelens die je in je lichaam 
kan hebben. Het is dan de bedoeling dat je je voorstelt dat jij deze sensatie of dit gevoel beleeft. 
Weer andere zinnen beschrijven emotionele situaties. Het is dan de bedoeling dat je je voorstelt dat 
je deze specifieke situatie meemaakt. 

Het gaat er hier altijd om dat je je voorstelt dat JIJ de ervaring hebt. Het gaat dus om een actie of 
expressie van jouw lichaam, een sensatie in jouw lichaam, of een situatie die jijzelf beleeft. 

Druk op één van de response knoppen om met de taak te beginnen."; 
			font =		"arial";		
			font_size = 16;
			
} introduction;

# Experimental text: sentence
text {caption = "test";} sentence;

# End
text {
			caption = 	"Dit is het einde van dit deel van het experiment."; 
			font =		"arial";		
			font_size = 16;} 
			end;

# --------------- SDL definitions: PICTURES --------------- #

# ITI
picture {background_color = 0,0,0;} ITI_picture;

# Intro
picture {text introduction; x = 0; y = 0;} introduction_picture;

picture {text { caption = "Wacht op eerste pulse"; font="arial"; font_size = 16;}; x=-60; y=0;} pulsetrial;

# End
picture {text end; x = 0; y = 0;} end_picture;

# Experimental picture
picture {text sentence; x = 0; y = 0;} experimental_picture;

# --------------- SDL definitions: TRIALS --------------- #

# Intro trial
trial {
	all_responses		= true; 
	trial_type 			= first_response;
	trial_duration 	= forever;
		stimulus_event {
		picture introduction_picture;
		time = 0;
		} introduction_event;
} introduction_trial;

# Experimental trial: ITI followed by sentence
trial {
	stimulus_event {
		picture experimental_picture;
		duration = 6000;
	} experimental_event;
} experimental_trial; 

# End trial
trial {
	trial_duration = 1000000; 
	stimulus_event {
		picture end_picture;
		delta_time = 2000;
	} end_event;
} end_trial;

# --------------- START OF PCL --------------- #
begin_pcl;

# Regular execution of intro trial
introduction_trial.present();

pulsetrial.present();
int currentpulse_count=pulse_manager.main_pulse_count();
loop until pulse_manager.main_pulse_count()-currentpulse_count>1 begin                   #waits for a pulse and shows instructions
end;

# Four non-randomized arrays with stimuli (3 w/category stimuli, 1 w/null events)
array <string> sentences_action[20] =
	{	"Hard wegrennen",
		"Iemand wegduwen",
		"Iemand stevig vastpakken",
		"Je hoofd schudden",
		"Heftige armgebaren maken",
		"Ergens voor terugdeinzen",
		"Je ogen dichtknijpen",
		"Je ogen wijd open sperren",
		"Je wenkbrauwen fronsen",
		"Je schouders ophalen",
		"Op de vloer stampen",
		"In elkaar duiken",
		"Je schouders laten hangen",
		"Je vuisten ballen",
		"Je borst vooruit duwen",
		"Je tanden op elkaar zetten",
		"Je hand voor je mond slaan",
		"Onrustig bewegen",
		"Heen en weer lopen",
		"Je hoofd afkeren",
};

array <string> sentences_interoception[20] =
	{	"Een brok in je keel",
		"Buiten adem zijn",
		"Een versnelde hartslag",
		"Je hart klopt in de keel",
		"Een benauwd gevoel",
		"Een misselijk gevoel",
		"Druk op je borst",
		"Strak aangespannen spieren",
		"Een droge keel",
		"Koude rillingen hebben",
		"Bloed stroomt naar je hoofd",
		"Een verdoofd gevoel",
		"Je hebt tintelende ledenmaten",
		"Een verlaagde hartslag",
		"Je hebt zware ledematen",
		"Een versnelde ademhaling",
		"Je hebt hoofdpijn",
		"Je hebt buikpijn",
		"Zweet staat in je handen",
		"Je maag keert zich om",
};

array <string> sentences_situation[20] =
	{	"Vals beschuldigd worden",
		"Dierbare overlijdt",
		"Vlees is bedorven",
		"Je wordt bijna aangereden",
		"Iemand naast je braakt",
		"Huis staat in brand",
		"Zonder reden ontslagen worden",
		"Een ongemakkelijke stilte",
		"Alleen in donker park",
		"Inbraak in je huis",
		"Een gewond dier zien",
		"Tentamen verknallen",
		"Je partner bedriegt je",
		"Dierbare is vermist",
		"Belangrijke sollicitatie vergeten",
		"Onvoorbereid presentatie geven",
		"Je baas beledigt je",
		"Goede vriend negeert je",
		"Slecht nieuws bij arts",
		"Bommelding in metro",
};

# This array (randomly) lists conditions which correspond to the stimuli (incl. null)
array <int> sentences_condition[72] =
	{	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
		2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
		3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
		4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
}; # 1 = action, 2 = interoception, 3 = situation, 4 = NULL-event

sentences_condition.shuffle(); 			# randomization of sentences-condition

# Three (one for each condition) arrays of length(category) of indices for sentence-arrays
array <int> index_action[0];
loop int i = 1 until i > 20 begin;
	index_action.add(i);		
	i = i + 1;
end;

index_action.shuffle();						#randomization of indices (--> random draw from sentence-arrays)
 
array <int> index_interoception[0];
loop int i = 1 until i > 20 begin;
	index_interoception.add(i);		
	i = i + 1;
end;

index_interoception.shuffle();			#randomization of indices
 
array <int> index_situation[0];
loop int i = 1 until i > 20 begin;
	index_situation.add(i);
	i = i + 1;
end;

index_situation.shuffle();					#randomization of indices

# Iteration-variables: keeping track of how many times a condition is presented already
# NB: no index-array or iteration-variable for NULL-events, because these are the same every time
int iteration_action = 0;
int iteration_interoception = 0;
int iteration_situation = 0;
int start_pic = 0;	
int start_null = 0;

# --- start the loop of the experimental_trial --- #	
loop int i = 1 until i > sentences_condition.count() begin;

	int sentence_category = sentences_condition[i]; # random condition is drawn
	
	# Condition = action
	if (sentence_category == 1) then
		iteration_action = iteration_action + 1;
		start_pic = clock.time();
		sentence.set_caption(sentences_action[index_action[iteration_action]]);
		sentence.redraw();
		experimental_event.set_event_code(string(index_action[iteration_action]+100));
		experimental_trial.present();
		ITI_picture.present();
		logfile.add_event_entry("ISI");
		loop until clock.time() > (start_pic+6000+2000) begin end;
	
	# Condition = interoception
	elseif (sentence_category == 2) then
		iteration_interoception = iteration_interoception + 1;
		start_pic = clock.time();
		sentence.set_caption(sentences_interoception[index_interoception[iteration_interoception]]);
		sentence.redraw();		
		experimental_event.set_event_code(string(index_interoception[iteration_interoception]+200));
	   experimental_trial.present();
		ITI_picture.present();
		logfile.add_event_entry("ISI");
		loop until clock.time() > (start_pic+6000+2000) begin end;
		
	# Condition = situation
	elseif (sentence_category == 3) then
		iteration_situation = iteration_situation + 1;
		start_pic = clock.time();
		sentence.set_caption(sentences_situation[index_situation[iteration_situation]]);
		sentence.redraw();
		experimental_event.set_event_code(string(index_situation[iteration_situation]+300));
	   experimental_trial.present();
		ITI_picture.present();
		logfile.add_event_entry("ISI");
		loop until clock.time() > (start_pic+6000+2000) begin end;
		
	# Condition = NULL-event
	elseif (sentence_category == 4) then
			start_null = clock.time();
			ITI_picture.present();
			logfile.add_event_entry("NULL");
			loop until clock.time() > (start_null+10000) begin end;
					
	end; # end of if-statement
	
	i = i + 1;

end; # end of loop

end_trial.present();


