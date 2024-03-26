

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(ontable b)
(on c b)
(on d e)
(ontable e)
(clear a)
(clear c)
)
(:goal
(and
(on c b)
(on d e)
(on e c))
)
)


