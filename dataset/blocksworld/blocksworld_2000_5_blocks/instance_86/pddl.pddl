

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(on b a)
(ontable c)
(on d e)
(ontable e)
(clear b)
(clear c)
)
(:goal
(and
(on a e)
(on d c)
(on e d))
)
)


