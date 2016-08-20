#ifndef MAIL_H
#define MAIL_H

#include<iostream>
#include <stdio.h>
#include <stdarg.h>

#include <string>
using namespace std;


class Mail {

public:
	Mail(string email = "") {
		file = fopen("test.txt", "w");
		if (file == NULL)
			cout << "Can not open" << endl;
		else
		{
			cout << "KITTI result" << endl;
		}
	}

	~Mail() {
		if (file) {
			fclose(file);
		}
	}

	void msg(const char *format, ...) {
		va_list args;
		va_start(args, format);
		if (file) {
			vfprintf(file, format, args);
			fprintf(file, "\n");
		}
		vprintf(format, args);
		printf("\n");
		va_end(args);
	}

private:

	//FILE *mail;
	FILE *file;

};



#endif
