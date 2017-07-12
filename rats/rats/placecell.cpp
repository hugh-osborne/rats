#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include <cstdlib>
#include <string>
#include <sstream>
#include <vector>
#include <iterator>
#include "placecell.hpp"
#include "hmm.hpp"

PlaceCell::PlaceCell(const char *filename, glm::vec4 col, bool use_hmm, GLfloat start_time, GLfloat end_time,const  char *output_filename) {
	colour = col;
	spike_bin_filename = output_filename;

	std::ifstream input(filename);

	for ( std::string line; std::getline(input, line); ) {
	times.push_back(std::atof(line.c_str()));
	}

	current_time = &(*times.begin());
	next_time = times.begin() + 1;

	if(use_hmm) {
		HMM *hmm = new HMM(this, start_time, end_time);

		std::deque<GLfloat> hmm_times = hmm->getSpikeTimes();
		if (!hmm_times.empty()) {
			times = hmm_times;
			current_time = &(*times.begin());
			next_time = times.begin() + 1;
		}
		else {
			next_time = times.end();
		}
		delete hmm;
	}

	input.close();
}

GLfloat *PlaceCell::checkNextTime() {
	if(next_time == times.end()) {
		return 0;
	}
	return &(*(next_time));
}

GLfloat *PlaceCell::getNextTime() {
	if(next_time == times.end()) {
		return 0;
	}

	current_time = &(*(next_time++));

	return current_time;
}

GLfloat *PlaceCell::getCurrentTime() {
	return current_time;
}

glm::vec4 PlaceCell::getColour() {
	return colour;
}

const char* PlaceCell::getOutputFilename() {
	return spike_bin_filename;
}
