#include <stdio.h>
#include <cstring>
#include <stdlib.h>
#include <iostream>
#include "defs.hpp"
#include "rat.hpp"
#include "../include/glm/glm.hpp"
#include <vector>
#include <fstream>
#include <cstdlib>
#include <string>
#include <sstream>
#include "kmeans.hpp"
#include "hmm.hpp"
#include "placefield.hpp"
#include "stringsplit.hpp"
#include "process.hpp"
#include "bitmap_image.hpp"

void Process::init(const char * inputfilename) {

	std::ifstream input(inputfilename);

	std::string field_coords_file;
	std::getline(input, field_coords_file);

	std::ofstream output(field_coords_file.c_str(),std::ofstream::out | std::ofstream::trunc);
	output << "track,day,run,unit,spike_rates\n";

	std::string current_run_filename("");
	Path current_path;

	for (std::string line; std::getline(input, line); ) {
		std::vector<std::string> chunks = StringSplit::split(line, ',');

		if( std::strcmp(chunks[0].c_str(), "track") == 0 ) { //first line - ignore.
			continue;
		}

		const char * track = chunks[0].c_str();
		const char * day = chunks[1].c_str();
		const char * run = chunks[2].c_str();
		const char * unit = chunks[3].c_str();
		const char * runfilename = chunks[4].c_str();
		const char * spikefilename = chunks[5].c_str();
		const char * outfilename = chunks[6].c_str();
		const char * imagefilename = chunks[7].c_str();

		printf("Process %s %s %s %s\n", track, day, run, unit);

		if(current_run_filename.compare(runfilename) != 0) {
			current_path = Path(runfilename);
			current_run_filename = std::string(runfilename);
		} else {
			current_path.reset();
		}

		PlaceCell pc = PlaceCell(spikefilename, glm::vec4(1.0f, 1.0f, 0.0f, 1.0f), true, current_path.getStartTime(), current_path.getEndTime(), outfilename);

		PlaceField pf = PlaceField();
		std::vector<std::vector<float> > spike_rates = pf.findMaxDivision(current_path, pc);

		glutPostRedisplay();
		glClear(GL_COLOR_BUFFER_BIT);
		pf.drawField();
		pf.drawBoxes();
		glFlush();

		writeRenderTexture(imagefilename);

		output << track << "," << day << "," << run << "," << unit;
		for (int i = 0; i < spike_rates.size(); i++) {
			for (int j = 0; j < spike_rates[i].size(); j++) {
				output << "," << spike_rates[i][j];
			}
		}

		output << "\n";

	}

	output.flush();
	output.close();
	input.close();

}

void Process::processInput(int argc, char** argv) {
	init(argv[1]/*"bon/bon_4/bon_process_input.txt"*/);
}

void Process::writeRenderTexture(const char *filename) {
	int width = 500;
	int height = 500;
	const size_t bytesPerPixel = 3;	// RGB
	const size_t imageSizeInBytes = bytesPerPixel * size_t(width) * size_t(height);

	// Allocate with malloc, because the data will be managed by wxImage
	unsigned char * pixels = (unsigned char *)malloc(imageSizeInBytes);

	// glReadPixels can align the first pixel in each row at 1-, 2-, 4- and 8-byte boundaries. We
	// have allocated the exact size needed for the image so we have to use 1-byte alignment
	// (otherwise glReadPixels would write out of bounds)
	glPixelStorei(GL_PACK_ALIGNMENT, 1);
	glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE, pixels);

	// glReadPixels reads the given rectangle from bottom-left to top-right, so we must
	// reverse it
	for(int y = 0; y < height / 2; y++)
	{
		const int swapY = height - y - 1;
		for(int x = 0; x < width; x++)
		{
			const int offset = int(bytesPerPixel) * (x + y * width);
			const int swapOffset = int(bytesPerPixel) * (x + swapY * width);

			// Swap R, G and B of the 2 pixels
			std::swap(pixels[offset + 0], pixels[swapOffset + 0]);
			std::swap(pixels[offset + 1], pixels[swapOffset + 1]);
			std::swap(pixels[offset + 2], pixels[swapOffset + 2]);
		}
	}

	bitmap_image image(width,height);
	image.clear();
	for(unsigned int i=0; i<width; i++) {
		for(unsigned int j=0; j<height; j++) {
			const int offset = int(bytesPerPixel) * (i + (j * width));
			image.set_pixel(i,j,pixels[offset+0],pixels[offset+1],pixels[offset+2]);
		}
	}
	image.save_image(filename);

	free(pixels);
}
