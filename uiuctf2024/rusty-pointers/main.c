#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define LEN 64
#define LEN2 2000
#define LEN3 80

typedef uint8_t u8;
typedef struct {
    u8* data;
    size_t len;
} RulesT;
typedef struct {
    u8 data[LEN];
} NotesT;
typedef struct {
    u8 data[LEN3];
} LawsT;

void menu() {
    printf("1. Create a Rule or Note\n");
    printf("2. Delete a Rule or Note\n");
    printf("3. Read a Rule or Note\n");
    printf("4. Edit a Rule or Note\n");
    printf("5. Make a Law\n");
    printf("6. Exit\n");
}

void submenu() {
    printf("1. Rules\n");
    printf("2. Notes\n");
}

void prompt() {
    printf("> ");
    fflush(stdout);
}

u8* get_rule() {
    u8* buffer = malloc(LEN);
    memset(buffer, 0, LEN);
    return buffer;
}

u8* get_law() {
    u8* buffer = malloc(LEN2);
    memset(buffer, 0, LEN2);
    return buffer;
}

NotesT get_note() {
    NotesT note;
    memset(&note, 0, sizeof(NotesT));
    return note;
}

void read_buf(u8* buf) {
    printf("Contents of Buffer:\n");
    for (int i = 0; i < LEN; i++) {
        printf("%02x ", buf[i]);
    }
    printf("\n");
    uint64_t v1 = ((uint64_t)buf[0] << 56) | ((uint64_t)buf[1] << 48) | ((uint64_t)buf[2] << 40) |
                  ((uint64_t)buf[3] << 32) | ((uint64_t)buf[4] << 24) | ((uint64_t)buf[5] << 16) |
                  ((uint64_t)buf[6] << 8) | buf[7];
    uint64_t v2 = ((uint64_t)buf[8] << 56) | ((uint64_t)buf[9] << 48) | ((uint64_t)buf[10] << 40) |
                  ((uint64_t)buf[11] << 32) | ((uint64_t)buf[12] << 24) | ((uint64_t)buf[13] << 16) |
                  ((uint64_t)buf[14] << 8) | buf[15];
    printf("%#016lx, %#016lx\n", v1, v2);
}

void edit_buf(u8* buf) {
    printf("Send up to %d bytes.\n", LEN);
    prompt();
    fgets((char*)buf, LEN, stdin);
    fflush(stdout);
}

void create_rule(RulesT** rules, size_t* len) {
    u8* buf = get_rule();
    RulesT* new_rules = realloc(*rules, sizeof(RulesT) * (*len + 1));
    if (!new_rules) {
        free(buf);
        exit(1);
    }
    *rules = new_rules;
    (*rules)[*len].data = buf;
    (*rules)[*len].len = LEN;
    (*len)++;
    printf("Rule Created!\n");
}

void create_note(NotesT** notes, size_t* len) {
    NotesT* new_notes = realloc(*notes, sizeof(NotesT) * (*len + 1));
    if (!new_notes) {
        exit(1);
    }
    *notes = new_notes;
    memset(&(*notes)[*len], 0, sizeof(NotesT));
    (*len)++;
    printf("Note Created!\n");
}

void make_law() {
    u8* bufa = malloc(LEN2);
    memset(bufa, 0, LEN2);
    u8* buf = get_law();
    memcpy(buf, bufa, LEN2);
    free(bufa);
    uint64_t v1 = ((uint64_t)buf[0] << 56) | ((uint64_t)buf[1] << 48) | ((uint64_t)buf[2] << 40) |
                  ((uint64_t)buf[3] << 32) | ((uint64_t)buf[4] << 24) | ((uint64_t)buf[5] << 16) |
                  ((uint64_t)buf[6] << 8) | buf[7];
    uint64_t v2 = ((uint64_t)buf[8] << 56) | ((uint64_t)buf[9] << 48) | ((uint64_t)buf[10] << 40) |
                  ((uint64_t)buf[11] << 32) | ((uint64_t)buf[12] << 24) | ((uint64_t)buf[13] << 16) |
                  ((uint64_t)buf[14] << 8) | buf[15];
    printf("%#016lx, %#016lx\n", v1, v2);
}

void delete_rule(RulesT** rules, size_t* len, size_t choice) {
    if (choice >= *len) {
        printf("OOB!\n");
    } else {
        free((*rules)[choice].data);
        for (size_t i = choice; i < *len - 1; i++) {
            (*rules)[i] = (*rules)[i + 1];
        }
        (*len)--;
        RulesT* new_rules = realloc(*rules, sizeof(RulesT) * (*len));
        if (!new_rules) {
            exit(1);
        }
        *rules = new_rules;
        printf("Rule Removed!\n");
    }
}

void delete_note(NotesT** notes, size_t* len, size_t choice) {
    if (choice >= *len) {
        printf("OOB!\n");
    } else {
        for (size_t i = choice; i < *len - 1; i++) {
            (*notes)[i] = (*notes)[i + 1];
        }
        (*len)--;
        NotesT* new_notes = realloc(*notes, sizeof(NotesT) * (*len));
        if (!new_notes) {
            exit(1);
        }
        *notes = new_notes;
        printf("Note Deleted!\n");
    }
}

void read_rule(RulesT* rules, size_t len, size_t choice) {
    if (choice >= len) {
        printf("OOB!\n");
    } else {
        read_buf(rules[choice].data);
    }
}

void read_note(NotesT* notes, size_t len, size_t choice) {
    if (choice >= len) {
        printf("OOB!\n");
    } else {
        read_buf(notes[choice].data);
    }
}

void edit_rule(RulesT* rules, size_t len, size_t choice) {
    if (choice >= len) {
        printf("OOB!\n");
    } else {
        edit_buf(rules[choice].data);
    }
}

void edit_note(NotesT* notes, size_t len, size_t choice) {
    if (choice >= len) {
        printf("OOB!\n");
    } else {
        edit_buf(notes[choice].data);
    }
}

void handle_create(RulesT** rules, size_t* rules_len, NotesT** notes, size_t* notes_len) {
    submenu();
    prompt();
    int choice;
    scanf("%d", &choice);
    if (choice == 1) {
        create_rule(rules, rules_len);
    } else if (choice == 2) {
        create_note(notes, notes_len);
    } else {
        printf("Invalid Choice!\n");
    }
}

void handle_edit(RulesT* rules, size_t rules_len, NotesT* notes, size_t notes_len) {
    submenu();
    prompt();
    int choice;
    scanf("%d", &choice);
    if (choice == 1) {
        edit_rule(rules, rules_len, 0);
    } else if (choice == 2) {
        edit_note(notes, notes_len, 0);
    } else {
        printf("Invalid Choice!\n");
    }
}

void handle_delete(RulesT** rules, size_t* rules_len, NotesT** notes, size_t* notes_len) {
    submenu();
    prompt();
    int choice;
    scanf("%d", &choice);
    if (choice == 1) {
        prompt();
        int rule_choice;
        scanf("%d", &rule_choice);
        delete_rule(rules, rules_len, rule_choice);
    } else if (choice == 2) {
        prompt();
        int note_choice;
        scanf("%d", &note_choice);
        delete_note(notes, notes_len, note_choice);
    } else {
        printf("Invalid Choice!\n");
    }
}

void handle_read(RulesT* rules, size_t rules_len, NotesT* notes, size_t notes_len) {
    submenu();
    prompt();
    int choice;
    scanf("%d", &choice);
    if (choice == 1) {
        prompt();
        int rule_choice;
        scanf("%d", &rule_choice);
        read_rule(rules, rules_len, rule_choice);
    } else if (choice == 2) {
        prompt();
        int note_choice;
        scanf("%d", &note_choice);
        read_note(notes, notes_len, note_choice);
    } else {
        printf("Invalid Choice!\n");
    }
}

int main() {
    RulesT* rules = NULL;
    size_t rules_len = 0;
    NotesT* notes = NULL;
    size_t notes_len = 0;
    int choice;
    while (1) {
        menu();
        prompt();
        scanf("%d", &choice);
        if (choice == 1) {
            handle_create(&rules, &rules_len, &notes, &notes_len);
        } else if (choice == 2) {
            handle_delete(&rules, &rules_len, &notes, &notes_len);
        } else if (choice == 3) {
            handle_read(rules, rules_len, notes, notes_len);
        } else if (choice == 4) {
            handle_edit(rules, rules_len, notes, notes_len);
        } else if (choice == 5) {
            make_law();
        } else if (choice == 6) {
            break;
        } else {
            printf("Invalid choice!\n");
        }
    }
    for (size_t i = 0; i < rules_len; i++) {
        free(rules[i].data);
    }
    free(rules);
    free(notes);
    return 0;
}

