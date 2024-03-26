

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(ontable c)
(on d e)
(ontable e)
(clear a)
(clear c)
(clear d)
)
(:goal
(and
(on b a)
(on c e)
(on e b))
)
)


