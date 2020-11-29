.SUFFIXES: .hny .tex

CODEDIR = ../../code

%.tex: $(CODEDIR)/%.hny
	python3 pp.py $< > $@

CODE = \
    BBhoare.tex \
    BBsema.tex \
    BBsemadata.tex \
    BBsematest.tex \
    Diners.tex \
    DinersAvoid.tex \
    DinersCV.tex \
    DinersSema.tex \
    Peterson.tex \
    PetersonInductive.tex \
    PetersonMethod.tex \
    RW.tex \
    RWbusychk.tex \
    RWcv.tex \
    RWfair.tex \
    RWlock.tex \
    RWmulti.tex \
    RWqtest.tex \
    RWqueue.tex \
    RWsbs.tex \
    RWtest.tex \
    Up.tex \
    UpEnter.tex \
    UpLock.tex \
    abp.tex \
    abptest.tex \
    actor.tex \
    actortest.tex \
    atm.tex \
    atomicinc.tex \
    baddblwait.tex \
    bank.tex \
    barrier.tex \
    barrier1.tex \
    barrier2.tex \
    barrier3.tex \
    busywait.tex \
    cs.tex \
    csTAS.tex \
    csbarebones.tex \
    csonebit.tex \
    dinersfix.tex \
    gpu.tex \
    hoare.tex \
    hoaremon.tex \
    hoaretest.tex \
    hw.tex \
    lockintf.tex \
    locksusp.tex \
    lst1.tex \
    lst2.tex \
    mesa.tex \
    naiveFlags.tex \
    naiveLock.tex \
    naiveTurn.tex \
    oo.tex \
    qbarrier.tex \
    queue.tex \
    queueMS.tex \
    queuetest.tex \
    qsort.tex \
    qsorttest.tex \
    semaphore.tex \
    spinlock.tex \
    spinlockInv.tex \
    stacktest.tex \
    stack1.tex \
    stack2.tex \
    stack3.tex \
    stack4.tex \
    trap.tex \
    trap2.tex \
    trap3.tex \
    trap4.tex \
    trap5.tex \
    trap6.tex \
    triangle.tex \
    xy.tex

all: $(CODE)
