class Draft:
    @classmethod
    def empty(cls):
        return cls([])
    
    def __len__(self):
        return len(self._draftList)