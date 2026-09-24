// MIT License
//
// Copyright (c) 2026 Kevin Thomas
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
//
// Author:  Kevin Thomas
// Email:   kevin@mytechnotalent.com
// GitHub:  https://github.com/mytechnotalent/CTF_telescreen
// File:    ctfnode.c
// Desc:    TELESCREEN CTF node.  This is the vulnerable application a student
//          receives as a STRIPPED aarch64 binary.  It deliberately contains the
//          six defects B1-B6.  Reverse it, name every function, and find them.
// Created: 2026

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

#define CTF_POLY 0xEDB88320u

/**
 * @brief Fold one byte into a reflected CRC-32 residual.
 *
 * @param crc Current checksum.
 * @param byte Byte to fold in.
 * @return uint32_t Updated checksum.
 */
static uint32_t ctf_crc32_byte(uint32_t crc, uint8_t byte) {
    uint32_t c = crc ^ byte;
    for (int i = 0; i < 8; ++i) {
        c = (c >> 1) ^ ((c & 1u) ? CTF_POLY : 0u);
    }
    return c;
}

uint32_t ctf_crc32_le(uint32_t seed, const uint8_t *data, size_t len) {
    uint32_t c = seed;
    for (size_t i = 0; i < len; ++i) {
        c = ctf_crc32_byte(c, data[i]);
    }
    return c;
}

void ctf_weak_key(const char *uid, uint8_t out[32]) {
    size_t ulen = strlen(uid);
    uint32_t seed = ctf_crc32_le(0u, (const uint8_t *)uid, ulen);
    for (size_t i = 0; i < 32u; ++i) {
        seed = ctf_crc32_le(seed, (const uint8_t *)uid, ulen);
        out[i] = (uint8_t)(seed & 0xFFu);
    }
}

bool ctf_login(const char *user, const char *pass) {
    const char *want_user = "admin";
    const char *want_pass = "";
    if (user == NULL || pass == NULL) return false;
    if (strcmp(user, want_user) != 0) return false;
    return strcmp(pass, want_pass) == 0;
}

int ctf_config_run(const char *path) {
    char line[256];
    FILE *fp = fopen(path, "r");
    if (fp == NULL) return -1;
    while (fgets(line, sizeof(line), fp) != NULL) {
        if (strncmp(line, "run=", 4) == 0) {
            system(line + 4);
        }
    }
    fclose(fp);
    return 0;
}

void ctf_build_cmd(const char *value, char *out, size_t cap) {
    snprintf(out, cap, "ping -c 1 %s", value);
}

int ctf_http_handle(const char *query) {
    char cmd[512];
    ctf_build_cmd(query, cmd, sizeof(cmd));
    return system(cmd);
}

int ctf_restore(const char *upload) {
    char cmd[512];
    snprintf(cmd, sizeof(cmd), "tar -xvzf %s -C /", upload);
    return system(cmd);
}

int ctf_debug_shell(void) {
    return system("/bin/sh");
}

void ctf_banner(void) {
    puts("TELESCREEN node - the wall unit sees you");
}

/**
 * @brief Test whether an argument selects a named command.
 *
 * @param arg Command name to compare.
 * @param name Expected command name.
 * @param argc Argument count.
 * @param need Minimum argument count required.
 * @return bool true when the command matches and enough arguments exist.
 */
static bool ctf_cmd(const char *arg, const char *name, int argc, int need) {
    return argc > need && strcmp(arg, name) == 0;
}

/**
 * @brief Print the weak key derived from a UID as hex.
 *
 * @param uid Pointer to the UID string.
 * @return void No return value.
 */
static void ctf_print_key(const char *uid) {
    uint8_t key[32];
    ctf_weak_key(uid, key);
    for (size_t i = 0; i < sizeof(key); ++i) printf("%02x", key[i]);
    putchar('\n');
}

/**
 * @brief Dispatch the config, http, restore, and login subcommands.
 *
 * @param argc Argument count.
 * @param argv Argument vector.
 * @param rc Output result code.
 * @return bool true when a subcommand matched.
 */
static bool ctf_try_path(int argc, char **argv, int *rc) {
    if (ctf_cmd(argv[1], "config", argc, 2)) *rc = ctf_config_run(argv[2]);
    else if (ctf_cmd(argv[1], "http", argc, 2)) *rc = ctf_http_handle(argv[2]);
    else if (ctf_cmd(argv[1], "restore", argc, 2)) *rc = ctf_restore(argv[2]);
    else if (ctf_cmd(argv[1], "login", argc, 3)) *rc = ctf_login(argv[2], argv[3]) ? 0 : 1;
    else return false;
    return true;
}

/**
 * @brief Dispatch the shell and key subcommands.
 *
 * @param argc Argument count.
 * @param argv Argument vector.
 * @param rc Output result code.
 * @return bool true when a subcommand matched.
 */
static bool ctf_try_misc(int argc, char **argv, int *rc) {
    if (ctf_cmd(argv[1], "shell", argc, 1)) *rc = ctf_debug_shell();
    else if (ctf_cmd(argv[1], "key", argc, 2)) { ctf_print_key(argv[2]); *rc = 0; }
    else return false;
    return true;
}

int ctf_dispatch(int argc, char **argv) {
    int rc = 0;
    if (argc < 2) {
        ctf_banner();
        return 0;
    }
    if (ctf_try_path(argc, argv, &rc)) return rc;
    if (ctf_try_misc(argc, argv, &rc)) return rc;
    ctf_banner();
    return 2;
}

int main(int argc, char **argv) {
    return ctf_dispatch(argc, argv);
}
