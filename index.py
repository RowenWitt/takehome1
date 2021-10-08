class Indexer():
    def __init__(self, body=[]):
        self.table = {}
        self.body = []

        self.add_to_table(body)

    def add_to_table(self, words):
        ''' Adds sequences to index table
        adds sequences to searchable body '''
        counter = 0
        for word in words:
            n_pos = len(self.body)
            self.body.append(word)

            for k in range(len(word) + 1):
                for j in range(k):
                    val = word[j:len(word) - (k - 1) + j]
                    counter += 1
                    if val in self.table:
                        self.table[val].add(n_pos)
                    else:
                        self.table[val] = {n_pos}

        return counter

    def search_indexes(self, pattern):
        ''' Search patterns and return indexes
        of matches '''
        out = []
        for seq in pattern:
            if seq in self.table:
                out.append(self.table[seq])
            else:
                pass

        return out

    def search(self, pattern):
        ''' Search patterns and return words
        of matches '''
        indexes = [list(i) for i in self.search_indexes(pattern)]
        out = []
        for i in indexes:
            out.append([self.body[j] for j in i])
        return out

    def reindex(self, body=[]):
        ''' Reindexes on an updated body,
        returns number of steps taken for
        triangular number check '''
        if body == []:
            body = self.body
        self.body = []
        self.table = {}
        count = self.add_to_table(body)
        return count

    def delete(self, values):
        ''' Reindexes without values to be deleted '''
        vals = [i for i in self.body if i not in values]
        self.reindex(vals)
